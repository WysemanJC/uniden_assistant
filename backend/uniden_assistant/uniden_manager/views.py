import json
import urllib.request
import tempfile
import uuid
import logging
import threading
from pathlib import Path
from urllib.error import HTTPError, URLError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

logger = logging.getLogger(__name__)

# In-memory storage for import progress (in production, use a cache like Redis)
import_progress_store = {}


class ProxyAPIView(APIView):
    """Proxy API that forwards requests to internal tiered APIs without direct DB access."""

    upstream_prefix = ''

    def _build_upstream_url(self, request, path_suffix=''):
        base = request.build_absolute_uri('/')[:-1]
        query = request.META.get('QUERY_STRING', '')
        path = f"/api/{self.upstream_prefix}{path_suffix}"
        url = f"{base}{path}"
        if query:
            url = f"{url}?{query}"
        return url

    def _proxy(self, request, path_suffix=''):
        url = self._build_upstream_url(request, path_suffix)
        data = request.body if request.method in ['POST', 'PUT', 'PATCH'] else None
        
        # Ensure data is bytes for urllib
        if data and not isinstance(data, bytes):
            data = data.encode('utf-8')
        
        # For empty POST/PUT/PATCH, send empty JSON object instead of None
        if request.method in ['POST', 'PUT', 'PATCH'] and not data:
            data = b'{}'
        
        headers = {
            'Content-Type': request.META.get('CONTENT_TYPE', 'application/json'),
        }
        
        req = urllib.request.Request(url, data=data, headers=headers, method=request.method)
        try:
            with urllib.request.urlopen(req) as resp:
                content = resp.read()
                try:
                    payload = json.loads(content.decode('utf-8'))
                    return Response(payload, status=resp.status)
                except json.JSONDecodeError:
                    return Response(content.decode('utf-8'), status=resp.status)
        except HTTPError as exc:
            content = exc.read().decode('utf-8')
            try:
                payload = json.loads(content)
                return Response(payload, status=exc.code)
            except json.JSONDecodeError:
                return Response({'error': content}, status=exc.code)
        except URLError as exc:
            return Response({'error': str(exc)}, status=502)


class HPDBProxyView(ProxyAPIView):
    upstream_prefix = 'hpdb/'

    def get(self, request, path=''):
        return self._proxy(request, path)

    def post(self, request, path=''):
        return self._proxy(request, path)


class UserSettingsProxyView(ProxyAPIView):
    upstream_prefix = 'usersettings/'

    def get(self, request, path=''):
        return self._proxy(request, path)

    def post(self, request, path=''):
        return self._proxy(request, path)

    def put(self, request, path=''):
        return self._proxy(request, path)

    def patch(self, request, path=''):
        return self._proxy(request, path)

    def delete(self, request, path=''):
        return self._proxy(request, path)


class AppConfigProxyView(ProxyAPIView):
    upstream_prefix = 'appconfig/'

    def get(self, request, path=''):
        return self._proxy(request, path)


class UnifiedImportViewSet(viewsets.ViewSet):
    """Unified import endpoint that detects file type and processes accordingly"""

    def _detect_directory_type(self, filenames):
        """
        Detect what type of directory was uploaded based on files present.
        Returns: dict with 'type', 'files', and 'description'
        """
        lower_names = [name.lower() for name in filenames]
        
        # Check for SD card root (has both HPDB and favorites_lists structure)
        has_hpdb_cfg = 'hpdb.cfg' in lower_names or any('hpdb/hpdb.cfg' in name.lower() for name in filenames)
        has_flist_cfg = 'f_list.cfg' in lower_names or any('favorites_lists/f_list.cfg' in name.lower() for name in filenames)
        has_system_files = any(name.lower().startswith('s_') and name.lower().endswith('.hpd') for name in lower_names)
        has_fav_files = any(name.lower().startswith('f_') and name.lower().endswith('.hpd') for name in lower_names)
        has_scanner_settings = any(
            'profile.cfg' in name.lower() or 
            'app_data.cfg' in name.lower() or 
            'scanner.inf' in name.lower() or 
            'discvery.cfg' in name.lower() or
            'discovery/' in name.lower()
            for name in filenames
        )
        
        # SD Card root detection (most comprehensive)
        if (has_hpdb_cfg or any('hpdb/' in name.lower() for name in filenames)) and \
           (has_flist_cfg or any('favorites_lists/' in name.lower() for name in filenames)):
            contains_list = ['HPDB database', 'Favourites']
            if has_scanner_settings:
                contains_list.append('Scanner settings')
            return {
                'type': 'sd_card',
                'description': 'SD Card Root Directory',
                'contains': ' and '.join(contains_list),
                'hpdb_files': [f for f in filenames if 'hpdb' in f.lower() or f.lower().startswith('s_')],
                'favorites_files': [f for f in filenames if 'favorites_lists' in f.lower() or f.lower().startswith('f_')],
                'scanner_settings': has_scanner_settings,
                'file_count': len(filenames)
            }
        
        # HPDB directory detection
        if has_hpdb_cfg and has_system_files:
            system_count = len([f for f in lower_names if f.startswith('s_') and f.endswith('.hpd')])
            return {
                'type': 'hpdb',
                'description': 'HPDB Database Directory',
                'contains': f'{system_count} system file(s)',
                'hpdb_files': filenames,
                'file_count': len(filenames)
            }
        
        # Favorites directory detection
        if has_flist_cfg and (has_fav_files or any(name.lower().endswith('.hpd') for name in lower_names)):
            hpd_count = len([f for f in lower_names if f.endswith('.hpd')])
            return {
                'type': 'favorites',
                'description': 'Favourites Directory',
                'contains': f'{hpd_count} favourites file(s)',
                'favorites_files': filenames,
                'file_count': len(filenames)
            }
        
        # Unknown/incomplete directory
        return {
            'type': 'unknown',
            'description': 'Unknown or incomplete directory',
            'contains': 'Cannot determine valid file structure',
            'file_count': len(filenames),
            'error': 'Directory must contain either HPDB files (hpdb.cfg + s_*.hpd) or Favourites files (f_list.cfg + f_*.hpd) or SD card root with both'
        }

    @action(detail=False, methods=['post'], url_path='detect')
    def detect(self, request):
        """Analyze uploaded files and return detection results for user confirmation"""
        files = request.FILES.getlist('files')
        if not files:
            return Response(
                {'error': 'No files uploaded'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        filenames = [f.name for f in files]
        detection = self._detect_directory_type(filenames)
        
        if detection['type'] == 'unknown':
            return Response(detection, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate a session ID for this upload
        session_id = str(uuid.uuid4())
        
        # Store files temporarily
        temp_dir = Path(tempfile.mkdtemp(prefix=f'uniden_import_{session_id}_'))
        for f in files:
            # Preserve directory structure from upload
            file_path = temp_dir / f.name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'wb') as out:
                for chunk in f.chunks():
                    out.write(chunk)
        
        return Response({
            'session_id': session_id,
            'detection': detection,
            'temp_path': str(temp_dir),
            'file_count': len(files)
        })

    @action(detail=False, methods=['post'], url_path='process')
    def process(self, request):
        """Start background import processing and return immediately with job ID"""
        session_id = request.data.get('session_id')
        import_mode = request.data.get('mode')
        import_type = request.data.get('type')
        temp_path = request.data.get('temp_path')
        
        if not all([session_id, import_mode, import_type, temp_path]):
            return Response(
                {'error': 'Missing required parameters'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if import_mode not in ['replace', 'merge']:
            return Response(
                {'error': 'Invalid mode. Must be "replace" or "merge"'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        temp_dir = Path(temp_path)
        if not temp_dir.exists():
            return Response(
                {'error': 'Session expired or invalid'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create a job ID for tracking progress
        job_id = str(uuid.uuid4())
        
        # Initialize progress tracking
        import_progress_store[job_id] = {
            'status': 'starting',
            'type': import_type,
            'stage': 'Initializing...',
            'current_file': '',
            'processed_files': 0,
            'total_files': 0,
            'current_records': 0,
            'total_records': 0,
            'hpdb_status': None,
            'favorites_status': None,
            'message': 'Starting import processing...'
        }
        
        # Start background processing thread
        thread = threading.Thread(
            target=self._process_import_background,
            args=(job_id, temp_dir, import_mode, import_type, request),
            daemon=True
        )
        thread.start()
        
        # Return immediately with job ID for polling
        return Response({
            'job_id': job_id,
            'status': 'started',
            'type': import_type,
            'message': f'Starting {import_type} import processing...'
        })

    def _process_import_background(self, job_id, temp_dir, import_mode, import_type, request):
        """Background thread to process import and update progress"""
        try:
            if import_type == 'sd_card':
                self._process_sd_card_with_progress(job_id, temp_dir, import_mode, request)
            elif import_type == 'hpdb':
                self._process_hpdb_with_progress(job_id, temp_dir, import_mode, request)
            elif import_type == 'favorites':
                self._process_favorites_with_progress(job_id, temp_dir, import_mode, request)
            
            import_progress_store[job_id]['status'] = 'completed'
            import_progress_store[job_id]['message'] = 'Import completed successfully'
        except Exception as e:
            logger.exception(f"Import job {job_id} failed", exc_info=e)
            import_progress_store[job_id]['status'] = 'failed'
            import_progress_store[job_id]['message'] = str(e)
        finally:
            # Cleanup temp directory
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except Exception:
                pass

    @action(detail=False, methods=['get'], url_path='progress')
    def get_progress(self, request):
        """Get the current progress of an import job"""
        job_id = request.query_params.get('job_id')
        if not job_id or job_id not in import_progress_store:
            return Response(
                {'error': 'Job not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(import_progress_store[job_id])

    def _process_hpdb_with_progress(self, job_id, temp_dir, mode, request):
        """Process HPDB files with progress tracking"""
        import_progress_store[job_id]['stage'] = 'Processing HPDB files...'
        import_progress_store[job_id]['status'] = 'processing'
        
        files = []
        for file_path in temp_dir.rglob('*'):
            if file_path.is_file():
                files.append(file_path)
        
        filenames = [f.name.lower() for f in files]
        if 'hpdb.cfg' not in filenames:
            raise Exception('Missing hpdb.cfg')
        if not any(name.startswith('s_') and name.endswith('.hpd') for name in filenames):
            raise Exception('Missing s_*.hpd system files')
        
        import_progress_store[job_id]['total_files'] = len(files)
        
        # Use the existing HPDB process method to store raw files and start job
        result = self._process_hpdb(temp_id=job_id, temp_dir=temp_dir, mode=mode, request=request)
        
        if 'error' in result:
            raise Exception(result['error'])
        
        import_progress_store[job_id]['hpdb_status'] = 'started'
        import_progress_store[job_id]['hpdb_job_id'] = result.get('job_id')
        import_progress_store[job_id]['message'] = f"HPDB import completed - job ID: {result.get('job_id')}"

    def _process_favorites_with_progress(self, job_id, temp_dir, mode, request):
        """Process favorites files with progress tracking"""
        import_progress_store[job_id]['stage'] = 'Processing Favourites files...'
        import_progress_store[job_id]['status'] = 'processing'
        
        files = []
        for file_path in temp_dir.rglob('*'):
            if file_path.is_file():
                files.append(file_path)
        
        filenames = [f.name.lower() for f in files]
        if 'f_list.cfg' not in filenames:
            raise Exception('Missing f_list.cfg')
        if not any(name.endswith('.hpd') for name in filenames):
            raise Exception('Missing .hpd files')
        
        # Parse f_list.cfg first to create FavoritesList records
        flist_path = next((f for f in files if f.name.lower() == 'f_list.cfg'), None)
        if flist_path:
            import_progress_store[job_id]['message'] = 'Parsing f_list.cfg...'
            from uniden_assistant.usersettings.hpdb_parser import FavoritesListParser
            try:
                FavoritesListParser.parse_favorites_list(str(flist_path))
                import_progress_store[job_id]['message'] = '✓ f_list.cfg parsed'
            except Exception as exc:
                logger.exception(f"Failed to parse f_list.cfg", exc_info=exc)
                import_progress_store[job_id]['message'] = f"✗ f_list.cfg failed: {str(exc)}"
        
        hpd_files = [f for f in files if f.name.lower().endswith('.hpd')]
        import_progress_store[job_id]['total_files'] = len(hpd_files)
        
        from uniden_assistant.usersettings.models import ScannerProfile
        from uniden_assistant.usersettings.parsers import UnidenFileParser
        
        parser = UnidenFileParser()
        imported = 0
        errors = []
        
        for idx, file_path in enumerate(hpd_files, 1):
            import_progress_store[job_id]['processed_files'] = idx - 1
            import_progress_store[job_id]['current_file'] = f"Processing {file_path.name}..."
            
            profile_name = file_path.stem.replace('_', ' ')
            profile, _ = ScannerProfile.objects.get_or_create(
                name=profile_name,
                defaults={'model': 'Uniden', 'firmware_version': ''}
            )
            
            try:
                with open(file_path, 'rb') as fh:
                    import_progress_store[job_id]['message'] = f"Parsing {file_path.name}..."
                    parser.parse(fh, profile)
                imported += 1
                import_progress_store[job_id]['message'] = f"✓ {file_path.name} imported"
            except Exception as exc:
                errors.append({'file': file_path.name, 'error': str(exc)})
                import_progress_store[job_id]['message'] = f"✗ {file_path.name} failed: {str(exc)}"
        
        import_progress_store[job_id]['processed_files'] = len(hpd_files)
        import_progress_store[job_id]['favorites_status'] = 'completed'
        import_progress_store[job_id]['message'] = f"Favourites import completed: {imported}/{len(hpd_files)} imported"

    def _process_sd_card_with_progress(self, job_id, temp_dir, mode, request):
        """Process SD card with progress tracking for both HPDB and Favourites"""
        import_progress_store[job_id]['stage'] = 'Processing SD Card contents...'
        import_progress_store[job_id]['message'] = 'Scanning for HPDB and Favourites...'
        
        # Try to process HPDB if present
        hpdb_dir = temp_dir / 'HPDB'
        if not hpdb_dir.exists():
            if (temp_dir / 'hpdb.cfg').exists():
                hpdb_dir = temp_dir
            else:
                hpdb_cfg_files = list(temp_dir.rglob('hpdb.cfg'))
                if hpdb_cfg_files:
                    hpdb_dir = hpdb_cfg_files[0].parent
        
        if hpdb_dir and hpdb_dir.exists() and (hpdb_dir / 'hpdb.cfg').exists():
            import_progress_store[job_id]['message'] = 'Found HPDB, starting import...'
            self._process_hpdb_with_progress(job_id, hpdb_dir, mode, request)
        
        # Try to process Favourites if present
        fav_dir = temp_dir / 'ubcdx36' / 'favorites_lists'
        if not fav_dir.exists():
            fav_dir = temp_dir / 'favorites_lists'
        if not fav_dir.exists():
            if (temp_dir / 'f_list.cfg').exists():
                fav_dir = temp_dir
            else:
                flist_cfg_files = list(temp_dir.rglob('f_list.cfg'))
                if flist_cfg_files:
                    fav_dir = flist_cfg_files[0].parent
        
        if fav_dir and fav_dir.exists() and (fav_dir / 'f_list.cfg').exists():
            import_progress_store[job_id]['message'] = 'Found Favourites, starting import...'
            self._process_favorites_with_progress(job_id, fav_dir, mode, request)

    def _process_hpdb(self, temp_id, temp_dir, mode, request):
        """Process HPDB files directly without modifying request"""
        import uuid
        import threading
        from pathlib import Path
        from uniden_assistant.hpdb.models import HPDBRawFile, HPDBRawLine, HPDBImportJob
        from django.conf import settings
        import logging
        
        logger = logging.getLogger(__name__)
        
        # Update progress
        if temp_id in import_progress_store:
            import_progress_store[temp_id]['message'] = 'Scanning HPDB files...'
        
        # Collect files
        files = []
        for file_path in temp_dir.rglob('*'):
            if file_path.is_file():
                files.append(file_path)
        
        # Validate required files
        filenames = [f.name.lower() for f in files]
        if 'hpdb.cfg' not in filenames:
            return {'type': 'hpdb', 'error': 'Missing hpdb.cfg'}
        if not any(name.startswith('s_') and name.endswith('.hpd') for name in filenames):
            return {'type': 'hpdb', 'error': 'Missing s_*.hpd system files'}
        
        if temp_id in import_progress_store:
            import_progress_store[temp_id]['message'] = f'Found {len(files)} HPDB files - preparing database...'
        
        # Create import job and store raw files directly
        job_id = str(uuid.uuid4())
        try:
            if temp_id in import_progress_store:
                import_progress_store[temp_id]['message'] = 'Creating HPDB import job...'
            
            job = HPDBImportJob.objects.using('hpdb').create(
                job_id=job_id,
                status='uploading',
                total_files=len(files),
                total_bytes=sum(f.stat().st_size for f in files)
            )
            
            if temp_id in import_progress_store:
                import_progress_store[temp_id]['message'] = 'Storing HPDB files in database...'
                import_progress_store[temp_id]['total_records'] = job.total_bytes
            
            file_ids = []
            total_lines = 0
            
            for file_idx, file_path in enumerate(files, 1):
                if temp_id in import_progress_store:
                    import_progress_store[temp_id]['current_file'] = file_path.name
                    import_progress_store[temp_id]['processed_files'] = file_idx - 1
                    import_progress_store[temp_id]['message'] = f'Reading {file_path.name} ({file_idx}/{len(files)})'
                
                file_size = file_path.stat().st_size
                raw_file = HPDBRawFile.objects.using('hpdb').create(
                    file_name=file_path.name,
                    file_type=file_path.suffix.lower(),
                    file_size=file_size
                )
                file_ids.append(raw_file.id)
                
                # Store file content line by line
                line_number = 0
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        line_number += 1
                        HPDBRawLine.objects.using('hpdb').create(
                            raw_file=raw_file,
                            line_number=line_number,
                            content=line
                        )
                        
                        total_lines += 1
                        # Update progress every 100 lines to avoid excessive updates
                        if total_lines % 100 == 0 and temp_id in import_progress_store:
                            import_progress_store[temp_id]['current_records'] = total_lines
                            import_progress_store[temp_id]['message'] = f'Storing {file_path.name}: {total_lines} lines processed'
                
                job.uploaded_files += 1
                job.uploaded_bytes += file_size
                job.save(update_fields=['uploaded_files', 'uploaded_bytes'])
                
                if temp_id in import_progress_store:
                    import_progress_store[temp_id]['message'] = f'✓ {file_path.name} stored ({line_number} lines)'
            
            if temp_id in import_progress_store:
                import_progress_store[temp_id]['processed_files'] = len(files)
                import_progress_store[temp_id]['current_records'] = total_lines
                import_progress_store[temp_id]['message'] = f'Stored {len(files)} files ({total_lines} total lines) - starting parse job...'
            
            # Update job status and start background processing
            job.status = 'uploaded'
            job.save()
            
            if temp_id in import_progress_store:
                import_progress_store[temp_id]['message'] = f'Background parsing started - job ID: {job_id}'
            
            # Start background processing thread
            from uniden_assistant.hpdb.views import _run_hpdb_import
            thread = threading.Thread(
                target=_run_hpdb_import,
                args=(job_id, file_ids),
                daemon=True
            )
            thread.start()
            
            return {
                'type': 'hpdb',
                'mode': mode,
                'job_id': job_id,
                'status': 'started'
            }
        except Exception as e:
            logger.exception("HPDB import failed", exc_info=e)
            if temp_id in import_progress_store:
                import_progress_store[temp_id]['message'] = f'✗ HPDB import failed: {str(e)}'
            return {'type': 'hpdb', 'error': str(e)}

    def _process_favorites(self, temp_dir, mode, request):
        """Process favorites files directly without modifying request"""
        from pathlib import Path
        from uniden_assistant.usersettings.models import ScannerProfile
        from uniden_assistant.parsers import UnidenFileParser
        from django.db.utils import DatabaseError
        import logging
        
        logger = logging.getLogger(__name__)
        
        # Collect files
        files = []
        for file_path in temp_dir.rglob('*'):
            if file_path.is_file():
                files.append(file_path)
        
        # Validate required files
        filenames = [f.name.lower() for f in files]
        if 'f_list.cfg' not in filenames:
            return {'type': 'favorites', 'error': 'Missing f_list.cfg'}
        if not any(name.endswith('.hpd') for name in filenames):
            return {'type': 'favorites', 'error': 'Missing .hpd files'}
        
        try:
            # Parse f_list.cfg first to create FavoritesList records
            flist_path = next((f for f in files if f.name.lower() == 'f_list.cfg'), None)
            if flist_path:
                from uniden_assistant.usersettings.hpdb_parser import FavoritesListParser
                try:
                    FavoritesListParser.parse_favorites_list(str(flist_path))
                except Exception as exc:
                    logger.exception(f"Failed to parse f_list.cfg", exc_info=exc)
            
            parser = UnidenFileParser()
            imported = 0
            errors = []
            
            for file_path in files:
                if not file_path.name.lower().endswith('.hpd'):
                    continue
                    
                profile_name = file_path.stem.replace('_', ' ')
                profile, _ = ScannerProfile.objects.get_or_create(
                    name=profile_name,
                    defaults={'model': 'Uniden', 'firmware_version': ''}
                )
                
                try:
                    with open(file_path, 'rb') as fh:
                        parser.parse(fh, profile)
                    imported += 1
                except Exception as exc:
                    errors.append({'file': file_path.name, 'error': str(exc)})
            
            return {
                'type': 'favorites',
                'mode': mode,
                'imported': imported,
                'errors': errors,
                'status': 'completed'
            }
        except DatabaseError as exc:
            logger.exception("Favorites import failed", exc_info=exc)
            return {'type': 'favorites', 'error': str(exc)}

    def _process_sd_card(self, temp_dir, mode, request):
        """Process SD card by forwarding both HPDB and favorites"""
        results = {'hpdb': None, 'favorites': None, 'settings': None}
        
        # Find HPDB directory
        hpdb_dir = temp_dir / 'HPDB'
        if not hpdb_dir.exists():
            # Files might be directly in temp_dir
            if (temp_dir / 'hpdb.cfg').exists():
                hpdb_dir = temp_dir
            else:
                # Search for hpdb.cfg
                hpdb_cfg_files = list(temp_dir.rglob('hpdb.cfg'))
                if hpdb_cfg_files:
                    hpdb_dir = hpdb_cfg_files[0].parent
        
        if hpdb_dir and hpdb_dir.exists() and (hpdb_dir / 'hpdb.cfg').exists():
            results['hpdb'] = self._process_hpdb(hpdb_dir, mode, request)
        
        # Find favorites directory
        fav_dir = temp_dir / 'ubcdx36' / 'favorites_lists'
        if not fav_dir.exists():
            fav_dir = temp_dir / 'favorites_lists'
        if not fav_dir.exists():
            # Files might be directly in temp_dir
            if (temp_dir / 'f_list.cfg').exists():
                fav_dir = temp_dir
            else:
                # Search for f_list.cfg
                flist_cfg_files = list(temp_dir.rglob('f_list.cfg'))
                if flist_cfg_files:
                    fav_dir = flist_cfg_files[0].parent
        
        if fav_dir and fav_dir.exists() and (fav_dir / 'f_list.cfg').exists():
            results['favorites'] = self._process_favorites(fav_dir, mode, request)
        
        # Process scanner settings files
        results['settings'] = self._process_scanner_settings(temp_dir)
        
        return {
            'type': 'sd_card',
            'mode': mode,
            'results': results,
            'status': 'completed'
        }

    def _process_scanner_settings(self, temp_dir):
        """Process scanner settings/profile configuration files and discovery data"""
        from uniden_assistant.usersettings.parsers import UnidenFileParser
        
        config_files = [
            temp_dir / 'ubcdx36' / 'profile.cfg',
            temp_dir / 'ubcdx36' / 'app_data.cfg',
            temp_dir / 'ubcdx36' / 'scanner.inf',
            temp_dir / 'ubcdx36' / 'discvery.cfg',
        ]
        
        parser = UnidenFileParser()
        processed = []
        errors = []
        
        # Process configuration files
        for cfg_path in config_files:
            if not cfg_path.exists():
                continue
            
            try:
                with open(cfg_path, 'rb') as f:
                    parser.store_records_only(f)
                processed.append(cfg_path.name)
            except Exception as exc:
                errors.append({'file': cfg_path.name, 'error': str(exc)})
        
        # Process discovery folder if it exists
        discovery_dir = temp_dir / 'ubcdx36' / 'discovery'
        if not discovery_dir.exists():
            discovery_dir = temp_dir / 'discovery'
        
        if discovery_dir.exists():
            try:
                for discovery_file in discovery_dir.rglob('*'):
                    if discovery_file.is_file():
                        try:
                            with open(discovery_file, 'rb') as f:
                                parser.store_records_only(f)
                            processed.append(f'discovery/{discovery_file.name}')
                        except Exception as exc:
                            errors.append({'file': f'discovery/{discovery_file.name}', 'error': str(exc)})
            except Exception as exc:
                errors.append({'file': 'discovery/', 'error': str(exc)})
        
        if not processed and not errors:
            return None
        
        return {
            'type': 'scanner_settings',
            'processed': processed,
            'errors': errors,
            'status': 'completed'
        }

    @action(detail=False, methods=['post'], url_path='cleanup')
    def cleanup(self, request):
        """Clean up temporary upload directories"""
        import shutil
        import glob
        
        try:
            # Find and remove all uniden_import_* directories in system temp
            temp_base = Path(tempfile.gettempdir())
            import_dirs = list(temp_base.glob('uniden_import_*'))
            
            removed_count = 0
            for dir_path in import_dirs:
                try:
                    shutil.rmtree(dir_path)
                    removed_count += 1
                except Exception as e:
                    logger.warning(f"Failed to remove temp directory {dir_path}: {e}")
            
            return Response({
                'status': 'success',
                'message': f'Cleaned up {removed_count} temporary upload directory(ies)',
                'removed_count': removed_count
            })
        except Exception as e:
            logger.exception("Cleanup failed", exc_info=e)
            return Response(
                {'error': f'Cleanup failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
