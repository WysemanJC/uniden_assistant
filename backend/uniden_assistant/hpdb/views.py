from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.utils import DatabaseError
from django.utils import timezone
import logging
from django.conf import settings
from pathlib import Path
import shutil
import threading
import uuid
import tempfile
from .models import (
    Country, State, County, HPDBAgency, HPDBChannelGroup, HPDBFrequency,
    HPDBRawFile, HPDBRawLine, HPDBImportJob, HPDBRectangle
)
from .serializers import (
    CountrySerializer, StateSerializer, CountySerializer, 
    HPDBAgencySerializer, HPDBChannelGroupSerializer, HPDBFrequencySerializer,
    HPDBTreeSerializer
)
from .hpdb_parser import HPDBParser

logger = logging.getLogger(__name__)


def _clear_hpdb_parsed_data():
    """Clear all parsed HPDB data but preserve raw file storage.
    
    This deletes all derived/parsed models (geography, agencies, groups, frequencies)
    while keeping the raw file data (HPDBRawFile, HPDBRawLine) for future re-parsing.
    Does NOT delete HPDBImportJob tracking records.
    
    Delete order respects foreign key dependencies (child before parent).
    """
    logger.info("Clearing all parsed HPDB data (keeping raw files)")
    
    # Delete in dependency order (children first)
    HPDBFrequency.objects.using('hpdb').all().delete()
    HPDBRectangle.objects.using('hpdb').all().delete()
    HPDBChannelGroup.objects.using('hpdb').all().delete()
    HPDBAgency.objects.using('hpdb').all().delete()
    County.objects.using('hpdb').all().delete()
    State.objects.using('hpdb').all().delete()
    Country.objects.using('hpdb').all().delete()
    
    logger.info("Cleared all parsed HPDB data successfully")


def _run_hpdb_import(job_id, file_ids, clear_existing=False):
    """Background task to process uploaded HPDB files"""
    try:
        job = HPDBImportJob.objects.using('hpdb').get(job_id=job_id)
        job.status = 'processing'
        job.save()

        if clear_existing:
            _clear_hpdb_parsed_data()
            job = HPDBImportJob.objects.using('hpdb').get(job_id=job_id)
            job.status = 'processing'
            job.save()

        def progress_callback(payload):
            job.processing_stage = payload.get('stage')
            job.current_file = payload.get('current_file')
            job.processed_files = payload.get('processed_files')
            job.total_files = payload.get('total_files')
            job.save(update_fields=['processing_stage', 'current_file', 'processed_files', 'total_files'])

        # Create temp directory and extract raw file data
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            raw_files = HPDBRawFile.objects.using('hpdb').filter(id__in=file_ids)
            
            for raw_file in raw_files:
                file_path = tmppath / raw_file.file_name
                lines = raw_file.lines.using('hpdb').all().order_by('line_number')
                with open(file_path, 'w', encoding='utf-8') as f:
                    for line_obj in lines:
                        f.write(line_obj.content)

            parser = HPDBParser(progress_callback=progress_callback)
            result = parser.parse_directory(str(tmppath))
            
            job.status = 'completed'
            job.result_data = result
            job.completed_at = timezone.now()
            job.save()
    except Exception as exc:
        logger.exception(f"HPDB import failed for job {job_id}", exc_info=exc)
        job = HPDBImportJob.objects.using('hpdb').get(job_id=job_id)
        job.status = 'failed'
        job.error_message = str(exc)
        job.completed_at = timezone.now()
        job.save()


def _hpdb_db_host():
    return settings.DATABASES.get('hpdb', {}).get('CLIENT', {}).get('host')


class HPDBStatsView(APIView):
    """Aggregate statistics for HPDB data."""

    def get(self, request):
        logger.info("HPDB stats request", extra={"host": _hpdb_db_host(), "env_path": str(settings.ENV_PATH)})
        try:
            agency_count = HPDBAgency.objects.using('hpdb').count()
            channel_group_count = HPDBChannelGroup.objects.using('hpdb').count()
            frequency_count = HPDBFrequency.objects.using('hpdb').count()

            system_type_counts = {
                'conventional': HPDBAgency.objects.using('hpdb').filter(system_type='Conventional').count(),
                'trunk': HPDBAgency.objects.using('hpdb').filter(system_type='Trunk').count(),
            }

            return Response({
                'countries': Country.objects.using('hpdb').count(),
                'states': State.objects.using('hpdb').count(),
                'counties': County.objects.using('hpdb').count(),
                'agencies': agency_count,
                'systems': agency_count,
                'departments': channel_group_count,
                'channel_groups': channel_group_count,
                'channels': frequency_count,
                'frequencies': frequency_count,
                'system_types': system_type_counts,
            })
        except DatabaseError as exc:
            logger.exception("HPDB stats query failed", exc_info=exc)
            return Response({
                'countries': 0,
                'states': 0,
                'counties': 0,
                'agencies': 0,
                'systems': 0,
                'departments': 0,
                'channel_groups': 0,
                'channels': 0,
                'frequencies': 0,
                'system_types': {'conventional': 0, 'trunk': 0},
                'error': str(exc),
                'host': _hpdb_db_host(),
            })


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Countries"""
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class StateViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for States"""
    queryset = State.objects.all()
    serializer_class = StateSerializer
    
    def get_queryset(self):
        queryset = State.objects.all()
        country_id_param = self.request.query_params.get('country', None)
        if country_id_param:
            # Filter by country's spec ID
            try:
                numeric_id = int(country_id_param.replace('country-', ''))
                queryset = queryset.filter(country__country_id=numeric_id)
            except (ValueError, TypeError):
                queryset = queryset.none()
        return queryset


class CountyViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Counties"""
    queryset = County.objects.all()
    serializer_class = CountySerializer
    
    def get_queryset(self):
        queryset = County.objects.all()
        state_id_param = self.request.query_params.get('state', None)
        if state_id_param:
            # Filter by state's spec ID
            try:
                numeric_id = int(state_id_param.replace('state-', ''))
                queryset = queryset.filter(state__state_id=numeric_id)
            except (ValueError, TypeError):
                queryset = queryset.none()
        return queryset


class HPDBAgencyViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for HPDB Agencies"""
    queryset = HPDBAgency.objects.all()
    serializer_class = HPDBAgencySerializer
    
    def get_queryset(self):
        queryset = HPDBAgency.objects.all()
        state_id_param = self.request.query_params.get('state', None)
        county_id_param = self.request.query_params.get('county', None)
        
        if state_id_param:
            try:
                numeric_id = int(state_id_param.replace('state-', ''))
                queryset = queryset.filter(states__state_id=numeric_id)
            except (ValueError, TypeError):
                queryset = queryset.none()
        
        if county_id_param:
            try:
                numeric_id = int(county_id_param.replace('county-', ''))
                queryset = queryset.filter(counties__county_id=numeric_id)
            except (ValueError, TypeError):
                queryset = queryset.none()
        
        return queryset.distinct()


class HPDBChannelGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for HPDB Channel Groups"""
    queryset = HPDBChannelGroup.objects.all()
    serializer_class = HPDBChannelGroupSerializer
    
    def get_queryset(self):
        queryset = HPDBChannelGroup.objects.using('hpdb').select_related('agency')
        
        # Filter by agency (primary filter)
        # Note: We filter by agency only, not by county/state, because:
        # 1. The agency is already scoped to the selected county
        # 2. Adding county/state filters forces expensive M2M lookups (1000x slower!)
        # 3. The frontend already passes the correct agency for the county
        # 
        # IMPORTANT: Filter by agency.agency_id directly, not via double underscore
        # Using agency__agency_id is 1000x slower than direct FK filter!
        agency_id_param = self.request.query_params.get('agency', None)
        if agency_id_param:
            try:
                numeric_id = int(agency_id_param.replace('agency-', ''))
                # First find the agency object with this agency_id
                agency_obj = HPDBAgency.objects.using('hpdb').filter(agency_id=numeric_id).first()
                if agency_obj:
                    queryset = queryset.filter(agency=agency_obj)
                else:
                    queryset = queryset.none()
            except (ValueError, TypeError):
                queryset = queryset.none()
        
        return queryset.distinct()


class HPDBFrequencyViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for HPDB Frequencies"""
    queryset = HPDBFrequency.objects.all()
    serializer_class = HPDBFrequencySerializer
    
    def get_queryset(self):
        queryset = HPDBFrequency.objects.using('hpdb').select_related('cgroup')
        
        # Support filtering by channel group - can accept either 'channel_group' or 'cgroup' parameter
        # Note: We only filter by channel_group, not by agency/county/state, because:
        # 1. The channel_group is already scoped to the selected agency/county
        # 2. Adding extra filters forces expensive M2M lookups
        # 3. Once we have the channel_group, we have all relevant frequencies
        # 
        # IMPORTANT: Filter by cgroup.cgroup_id directly, not via double underscore
        # Using cgroup__cgroup_id is 1000x slower than direct FK filter!
        cgroup_param = self.request.query_params.get('channel_group') or self.request.query_params.get('cgroup')
        if cgroup_param:
            try:
                numeric_id = int(cgroup_param.replace('cgroup-', ''))
                # First find the channel group object with this cgroup_id
                cgroup_obj = HPDBChannelGroup.objects.using('hpdb').filter(cgroup_id=numeric_id).first()
                if cgroup_obj:
                    queryset = queryset.filter(cgroup=cgroup_obj)
                else:
                    queryset = queryset.none()
            except (ValueError, TypeError):
                try:
                    queryset = queryset.filter(cgroup_id=int(cgroup_param))
                except (ValueError, TypeError):
                    queryset = queryset.none()
        
        return queryset.distinct()


class HPDBTreeViewSet(viewsets.ViewSet):
    """ViewSet for HPDB hierarchical tree view"""
    
    @action(detail=False, methods=['get'], url_path='tree')
    def tree(self, request):
        """Get hierarchical tree: Country > State (lazy load counties and agencies)"""
        tree = []
        
        # Only load countries and states initially - counties/agencies will be lazy-loaded
        for country in Country.objects.using('hpdb').all():
            country_node = {
                'id': f'country-{str(country.country_id)}',
                'type': 'country',
                'name_tag': country.name_tag,
                'code': country.code,
                'children': []
            }
            
            for state in country.states.using('hpdb').exclude(name_tag='_MultipleStates'):
                state_node = {
                    'id': f'state-{str(state.state_id)}',
                    'type': 'state',
                    'name_tag': state.name_tag,
                    'short_name': state.short_name,
                    'state_id': state.state_id,
                    'lazy': True  # Mark for lazy loading of counties
                }
                country_node['children'].append(state_node)
            
            if country_node['children']:
                tree.append(country_node)
        
        return Response(tree)
    
    @action(detail=False, methods=['get'], url_path='counties')
    def counties(self, request):
        """Get counties for a specific state (lazy load endpoint)"""
        state_id_param = request.query_params.get('state')
        if not state_id_param:
            return Response({'error': 'state parameter required'}, status=400)
        
        try:
            # Extract numeric ID from state parameter (e.g., "state-12" -> 12)
            numeric_id = int(state_id_param.replace('state-', ''))
            state = State.objects.using('hpdb').get(state_id=numeric_id)
        except (State.DoesNotExist, ValueError):
            return Response({'error': 'State not found'}, status=404)
        
        # Get all counties for this state that have agencies (in single query with aggregation)
        counties_with_agencies = (
            state.counties.using('hpdb')
            .filter(hpdb_agencies__isnull=False)
            .distinct()
            .order_by('name_tag')
        )
        
        counties = []
        
        # Check for statewide agencies (agencies in this state but not tied to specific counties)
        statewide_agencies = (
            HPDBAgency.objects.using('hpdb')
            .filter(states=state)
            .exclude(counties__state=state)
            .distinct()
        )
        
        if statewide_agencies.exists():
            # Add a pseudo-county for statewide agencies
            counties.append({
                'id': f'statewide-{state.state_id}',
                'type': 'statewide',
                'name_tag': 'Statewide',
                'state_id': state.state_id,
                'lazy': True
            })
        
        for county in counties_with_agencies:
            county_node = {
                'id': f'county-{str(county.county_id)}',
                'type': 'county',
                'name_tag': county.name_tag,
                'county_id': county.county_id,
                'lazy': True  # Counties lazy-load agencies
            }
            counties.append(county_node)
        
        return Response(counties)
    
    @action(detail=False, methods=['get'], url_path='agencies')
    def agencies(self, request):
        """Get agencies for a specific county or statewide agencies (lazy load endpoint)"""
        county_id_param = request.query_params.get('county')
        if not county_id_param:
            return Response({'error': 'county parameter required'}, status=400)
        
        agencies = []
        
        # Check if this is a statewide request
        if county_id_param.startswith('statewide-'):
            try:
                state_id = int(county_id_param.replace('statewide-', ''))
                state = State.objects.using('hpdb').get(state_id=state_id)
                
                # Get agencies in this state that are NOT tied to any county in the state
                statewide_agencies = (
                    HPDBAgency.objects.using('hpdb')
                    .filter(states=state)
                    .exclude(counties__state=state)
                    .distinct()
                )
                
                for agency in statewide_agencies:
                    agency_node = {
                        'id': f'agency-{str(agency.agency_id)}',
                        'type': 'agency',
                        'name_tag': agency.name_tag,
                        'agency_id': agency.agency_id,
                        'system_type': agency.system_type,
                        'enabled': agency.enabled,
                        'group_count': agency.channel_groups.using('hpdb').count()
                    }
                    agencies.append(agency_node)
            except (State.DoesNotExist, ValueError):
                return Response({'error': 'State not found'}, status=404)
        else:
            try:
                # Extract numeric ID from county parameter (e.g., "county-268" -> 268)
                numeric_id = int(county_id_param.replace('county-', ''))
                county = County.objects.using('hpdb').get(county_id=numeric_id)
            except (County.DoesNotExist, ValueError):
                return Response({'error': 'County not found'}, status=404)
            
            for agency in HPDBAgency.objects.using('hpdb').filter(counties=county):
                agency_node = {
                    'id': f'agency-{str(agency.agency_id)}',
                    'type': 'agency',
                    'name_tag': agency.name_tag,
                    'agency_id': agency.agency_id,
                    'system_type': agency.system_type,
                    'enabled': agency.enabled,
                    'group_count': agency.channel_groups.using('hpdb').count()
                }
                agencies.append(agency_node)
        
        return Response(agencies)


class HPDBImportViewSet(viewsets.ViewSet):
    """Upload HPDB data files (stage 1 of 2-step import)"""

    def create(self, request):
        """Upload HPDB files and store raw data in database"""
        files = request.FILES.getlist('files')
        if not files:
            return Response({'error': 'No files uploaded.'}, status=status.HTTP_400_BAD_REQUEST)

        filenames = [Path(f.name).name.lower() for f in files]
        if 'hpdb.cfg' not in filenames:
            return Response({'error': 'Missing hpdb.cfg.'}, status=status.HTTP_400_BAD_REQUEST)
        if not any(name.startswith('s_') and name.endswith('.hpd') for name in filenames):
            return Response({'error': 'Missing s_*.hpd system files.'}, status=status.HTTP_400_BAD_REQUEST)

        job_id = str(uuid.uuid4())
        system_files = [name for name in filenames if name.startswith('s_') and name.endswith('.hpd')]
        
        try:
            # Create import job
            job = HPDBImportJob.objects.using('hpdb').create(
                job_id=job_id,
                status='uploading',
                total_files=len(files),
                total_bytes=sum(f.size for f in files)
            )

            # Store raw files and lines in database
            file_ids = []
            for f in files:
                file_size = f.size
                raw_file = HPDBRawFile.objects.using('hpdb').create(
                    file_name=Path(f.name).name,
                    file_type=Path(f.name).suffix.lower(),
                    file_size=file_size
                )
                file_ids.append(raw_file.id)
                
                # Store file content line by line
                line_number = 0
                content = f.read().decode('utf-8', errors='ignore')
                for line in content.splitlines(keepends=True):
                    line_number += 1
                    HPDBRawLine.objects.using('hpdb').create(
                        raw_file=raw_file,
                        line_number=line_number,
                        content=line
                    )
                
                job.uploaded_files += 1
                job.uploaded_bytes += file_size
                job.save(update_fields=['uploaded_files', 'uploaded_bytes'])

            # Update job status and start background processing
            job.status = 'uploaded'
            job.save()

            # Start background processing thread
            thread = threading.Thread(
                target=_run_hpdb_import,
                args=(job_id, file_ids),
                daemon=True
            )
            thread.start()

            return Response(
                {
                    'job_id': job_id,
                    'message': 'Files uploaded successfully. Processing in background.'
                },
                status=status.HTTP_202_ACCEPTED
            )
        except Exception as e:
            logger.exception("HPDB upload failed", exc_info=e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class HPDBImportProgressView(APIView):
    """Get progress for an HPDB import job from database"""

    def get(self, request):
        job_id = request.query_params.get('job_id')
        if not job_id:
            return Response({'error': 'Missing job_id.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            job = HPDBImportJob.objects.using('hpdb').get(job_id=job_id)
            response_data = {
                'job_id': job.job_id,
                'status': job.status,
                'stage': job.processing_stage,
                'current_file': job.current_file,
                'processed_files': job.processed_files,
                'total_files': job.total_files,
                'uploaded_files': job.uploaded_files,
                'uploaded_bytes': job.uploaded_bytes,
                'total_bytes': job.total_bytes,
                'error_message': job.error_message,
                'result': job.result_data if job.status == 'completed' else None
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except HPDBImportJob.DoesNotExist:
            return Response({'error': 'Invalid job_id.'}, status=status.HTTP_404_NOT_FOUND)


class HPDBReloadFromRawView(APIView):
    """Rebuild HPDB data from stored raw files without re-upload.
    
    This endpoint re-parses the previously loaded HPDB data from the raw file storage.
    All parsed data (countries, states, counties, agencies, groups, frequencies) is
    cleared and rebuilt, but the raw file data itself is preserved for future reuse.
    """

    def post(self, request):
        try:
            logger.info("Starting HPDB re-parse from stored raw files")
            
            raw_files = HPDBRawFile.objects.using('hpdb').all()
            if not raw_files.exists():
                logger.warning("No raw HPDB files found in database")
                return Response({'error': 'No raw HPDB files found.'}, status=status.HTTP_400_BAD_REQUEST)

            filenames = [Path(f.file_name).name.lower() for f in raw_files]
            if 'hpdb.cfg' not in filenames:
                logger.warning("Missing hpdb.cfg in raw files")
                return Response({'error': 'Missing hpdb.cfg in raw files.'}, status=status.HTTP_400_BAD_REQUEST)
            if not any(name.startswith('s_') and name.endswith('.hpd') for name in filenames):
                logger.warning("Missing s_*.hpd system files in raw files")
                return Response({'error': 'Missing s_*.hpd system files in raw files.'}, status=status.HTTP_400_BAD_REQUEST)

            # Clear existing parsed data (but keep raw files and jobs)
            HPDBImportJob.objects.using('hpdb').all().delete()

            job_id = str(uuid.uuid4())
            file_ids = list(raw_files.values_list('id', flat=True))
            total_size = sum(raw_files.values_list('file_size', flat=True))

            job = HPDBImportJob.objects.using('hpdb').create(
                job_id=job_id,
                status='uploaded',
                total_files=len(file_ids),
                total_bytes=total_size
            )
            
            logger.info(f"Created re-parse job {job_id} for {len(file_ids)} files ({total_size} bytes)")

            thread = threading.Thread(
                target=_run_hpdb_import,
                args=(job_id, file_ids, True),  # True = clear_existing
                daemon=True
            )
            thread.start()

            return Response(
                {
                    'job_id': job_id,
                    'message': 'Rebuilding HPDB from raw files in background.'
                },
                status=status.HTTP_202_ACCEPTED
            )
        except Exception as exc:
            logger.exception("HPDB reparse from raw failed", exc_info=exc)
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)


class ClearHPDBDataView(APIView):
    """Clear all HPDB data from the database"""

    def post(self, request):
        try:
            logger.info("Clearing HPDB data")
            # Delete all HPDB records in reverse dependency order
            HPDBFrequency.objects.using('hpdb').all().delete()
            HPDBRectangle.objects.using('hpdb').all().delete()
            HPDBChannelGroup.objects.using('hpdb').all().delete()
            HPDBAgency.objects.using('hpdb').all().delete()
            County.objects.using('hpdb').all().delete()
            State.objects.using('hpdb').all().delete()
            Country.objects.using('hpdb').all().delete()
            
            logger.info("HPDB data cleared successfully")
            return Response({'message': 'HPDB data cleared successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Failed to clear HPDB data", exc_info=e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ClearHPDBRawDataView(APIView):
    """Clear all raw HPDB file data from the database"""

    def post(self, request):
        try:
            logger.info("Clearing HPDB raw data")
            # Delete raw files and lines (cascades to lines automatically)
            HPDBRawFile.objects.using('hpdb').all().delete()
            
            logger.info("HPDB raw data cleared successfully")
            return Response({'message': 'HPDB raw data cleared successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Failed to clear HPDB raw data", exc_info=e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CancelImportView(APIView):
    """Cancel in-progress HPDB import and clear job queue"""

    def post(self, request):
        try:
            logger.info("Cancelling HPDB import and clearing job queue")
            
            # Mark all non-completed jobs as cancelled
            active_jobs = HPDBImportJob.objects.using('hpdb').exclude(
                status__in=['completed', 'failed', 'cancelled']
            )
            
            cancelled_count = active_jobs.update(status='cancelled')
            
            logger.info(f"Cancelled {cancelled_count} import job(s)")
            
            return Response({
                'message': f'Cancelled {cancelled_count} import job(s)',
                'jobs_cancelled': cancelled_count
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Failed to cancel import", exc_info=e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
