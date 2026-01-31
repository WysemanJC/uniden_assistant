from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.utils import DatabaseError
import logging
from django.shortcuts import get_object_or_404
from django.conf import settings
from pathlib import Path
from .models import (
    ScannerProfile, Frequency, ChannelGroup, Agency, FavoritesList
)
from .serializers import (
    ScannerProfileSerializer, FrequencySerializer, ChannelGroupSerializer, 
    AgencySerializer, FavoritesListSerializer
)
from .parsers import UnidenFileParser
import tempfile

logger = logging.getLogger(__name__)


def _favorites_db_host():
    return settings.DATABASES.get('favorites', {}).get('CLIENT', {}).get('host')


class UserSettingsStatsView(APIView):
    """Aggregate statistics for user settings and favourites data."""

    def get(self, request):
        logger.info("Favourites stats request", extra={"host": _favorites_db_host(), "env_path": str(settings.ENV_PATH)})
        try:
            frequency_count = Frequency.objects.using('favorites').count()
            channel_group_count = ChannelGroup.objects.using('favorites').count()

            return Response({
                'profiles': ScannerProfile.objects.using('favorites').count(),
                'favorites_lists': FavoritesList.objects.using('favorites').count(),
                'agencies': Agency.objects.using('favorites').count(),
                'channel_groups': channel_group_count,
                'channels': frequency_count,
                'frequencies': frequency_count,
            })
        except DatabaseError as exc:
            logger.exception("Favourites stats query failed", exc_info=exc)
            return Response({
                'profiles': 0,
                'favorites_lists': 0,
                'agencies': 0,
                'channel_groups': 0,
                'channels': 0,
                'frequencies': 0,
                'error': str(exc),
                'host': _favorites_db_host(),
            })


class ScannerProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for Scanner Profiles"""
    queryset = ScannerProfile.objects.all()
    serializer_class = ScannerProfileSerializer

    @action(detail=True, methods=['post'])
    def upload_file(self, request, pk=None):
        """Upload and parse a Uniden configuration file"""
        profile = self.get_object()
        
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']
        
        try:
            parser = UnidenFileParser()
            parser.parse(file, profile)
            return Response({'success': True, 'profile': ScannerProfileSerializer(profile).data})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def export(self, request, pk=None):
        """Export profile to Uniden format"""
        profile = self.get_object()
        
        try:
            parser = UnidenFileParser()
            file_content = parser.export(profile)
            return Response({'content': file_content}, content_type='text/plain')
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FrequencyViewSet(viewsets.ModelViewSet):
    """ViewSet for Frequencies"""
    serializer_class = FrequencySerializer

    def get_queryset(self):
        profile_id = self.request.query_params.get('profile', None)
        if profile_id:
            return Frequency.objects.filter(profile_id=profile_id)
        return Frequency.objects.all()

    def perform_create(self, serializer):
        profile_id = self.request.data.get('profile')
        profile = get_object_or_404(ScannerProfile, id=profile_id)
        serializer.save(profile=profile)


class ChannelGroupViewSet(viewsets.ModelViewSet):
    """ViewSet for Channel Groups"""
    serializer_class = ChannelGroupSerializer

    def get_queryset(self):
        profile_id = self.request.query_params.get('profile', None)
        if profile_id:
            return ChannelGroup.objects.filter(profile_id=profile_id)
        return ChannelGroup.objects.all()

    def perform_create(self, serializer):
        profile_id = self.request.data.get('profile')
        profile = get_object_or_404(ScannerProfile, id=profile_id)
        serializer.save(profile=profile)


class AgencyViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Agencies (read-only)"""
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer


class SDCardViewSet(viewsets.ViewSet):
    """ViewSet for SD card import/export"""

    def _favorites_dir(self):
        base_dir = Path(settings.UNIDEN_DATA_DIR).expanduser().resolve()
        return base_dir / 'uniden' / 'ubcdx36' / 'favorites_lists'

    @action(detail=False, methods=['post'], url_path='import')
    def import_sd(self, request):
        """Import favorites from SD card path"""
        sd_path = request.data.get('path')
        if not sd_path:
            return Response({'error': 'No path provided'}, status=status.HTTP_400_BAD_REQUEST)

        sd_path = Path(sd_path).expanduser().resolve()
        if not sd_path.exists():
            return Response({'error': 'Path does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        favorites_dir = self._favorites_dir()
        favorites_dir.mkdir(parents=True, exist_ok=True)

        try:
            files = list(sd_path.glob('*.hpd')) + list(sd_path.glob('f_list.cfg'))
            if not files:
                return Response({'error': 'No .hpd or f_list.cfg files found'}, status=status.HTTP_400_BAD_REQUEST)

            for f in files:
                dest = favorites_dir / f.name
                dest.write_bytes(f.read_bytes())

            return Response({'success': True, 'files_imported': len(files)})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='export')
    def export_sd(self, request):
        """Export all profiles to SD card format"""
        profiles = ScannerProfile.objects.all()
        
        exported = []
        errors = []
        
        for profile in profiles:
            try:
                parser = UnidenFileParser()
                file_content = parser.export(profile)
                exported.append({'profile': profile.name, 'content': file_content})
            except Exception as exc:
                errors.append({'profile': profile.name, 'error': str(exc)})

        return Response({'exported': exported, 'errors': errors})


class FavoritesListViewSet(viewsets.ModelViewSet):
    """ViewSet for Favorites Lists"""
    queryset = FavoritesList.objects.all()
    serializer_class = FavoritesListSerializer
    
    @action(detail=True, methods=['get'], url_path='detail')
    def favorite_detail(self, request, pk=None):
        """Get detailed channel information from favorite's .hpd file"""
        favorite = self.get_object()
        
        favorites_dir = Path(settings.UNIDEN_DATA_DIR).expanduser().resolve() / 'uniden' / 'ubcdx36' / 'favorites_lists'
        hpd_file = favorites_dir / favorite.filename
        
        if not hpd_file.exists():
            return Response({'error': f'File not found: {favorite.filename}'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            groups = []
            current_group = None
            group_counter = 1
            freq_counter = 1
            
            with open(hpd_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('TargetModel') or line.startswith('FormatVersion'):
                        continue
                    
                    parts = line.split('\t')
                    if len(parts) < 2:
                        continue
                    
                    record_type = parts[0]
                    
                    if record_type == 'C-Group':
                        try:
                            name = ''
                            for i in range(1, len(parts)):
                                if parts[i].strip() and parts[i].strip() not in ['On', 'Off']:
                                    name = parts[i].strip()
                                    break
                            
                            if name:
                                current_group = {'id': group_counter, 'name': name, 'frequencies': []}
                                groups.append(current_group)
                                group_counter += 1
                        except (ValueError, IndexError):
                            pass
                    
                    elif record_type == 'C-Freq':
                        try:
                            freq_name = ''
                            frequency = None
                            modulation = ''
                            
                            for i in range(1, min(6, len(parts))):
                                if parts[i].strip() and parts[i].strip() not in ['On', 'Off']:
                                    freq_name = parts[i].strip()
                                    break
                            
                            if len(parts) > 5:
                                freq_str = parts[5].strip()
                                if freq_str.isdigit():
                                    frequency = int(freq_str)
                            
                            if len(parts) > 6:
                                modulation = parts[6].strip()
                            
                            if frequency and freq_name:
                                freq_entry = {
                                    'id': freq_counter,
                                    'name': freq_name,
                                    'frequency': frequency,
                                    'frequency_mhz': f"{frequency / 1000000:.4f} MHz",
                                    'modulation': modulation
                                }
                                freq_counter += 1
                                
                                if current_group:
                                    current_group['frequencies'].append(freq_entry)
                                else:
                                    if not groups:
                                        current_group = {'id': group_counter, 'name': 'Default Group', 'frequencies': []}
                                        groups.append(current_group)
                                        group_counter += 1
                                    else:
                                        current_group = groups[0]
                                    current_group['frequencies'].append(freq_entry)
                        except (ValueError, IndexError):
                            pass
            
            return Response({
                'name': favorite.name,
                'filename': favorite.filename,
                'groups': groups,
                'total_groups': len(groups),
                'total_frequencies': sum(len(g['frequencies']) for g in groups)
            })
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FavoritesImportViewSet(viewsets.ViewSet):
    """Import favorites from uploaded files"""

    def create(self, request):
        files = request.FILES.getlist('files')
        if not files:
            return Response({'error': 'No files uploaded.'}, status=status.HTTP_400_BAD_REQUEST)

        filenames = [Path(f.name).name.lower() for f in files]
        if 'f_list.cfg' not in filenames:
            return Response({'error': 'Missing f_list.cfg.'}, status=status.HTTP_400_BAD_REQUEST)
        if not any(name.endswith('.hpd') for name in filenames):
            return Response({'error': 'Missing .hpd files.'}, status=status.HTTP_400_BAD_REQUEST)

        temp_dir = Path(tempfile.mkdtemp(prefix='uniden_favorites_'))
        try:
            saved = {}
            for f in files:
                target = temp_dir / Path(f.name).name
                with open(target, 'wb') as out:
                    for chunk in f.chunks():
                        out.write(chunk)
                saved[Path(f.name).name.lower()] = target

            parser = UnidenFileParser()
            imported = 0
            errors = []
            for name, path in saved.items():
                if not name.endswith('.hpd'):
                    continue
                profile_name = path.stem.replace('_', ' ')
                profile, _ = ScannerProfile.objects.get_or_create(
                    name=profile_name,
                    defaults={'model': 'Uniden', 'firmware_version': ''}
                )
                try:
                    with open(path, 'rb') as fh:
                        parser.parse(fh, profile)
                    imported += 1
                except Exception as exc:
                    errors.append({'file': path.name, 'error': str(exc)})

            return Response({
                'imported': imported,
                'errors': errors
            })
        except DatabaseError as exc:
            return Response(
                {'error': str(exc), 'host': _favorites_db_host()},
                status=status.HTTP_400_BAD_REQUEST
            )
        except DatabaseError as exc:
            logger.exception("Favourites import failed", exc_info=exc)
            return Response(
                {'error': str(exc), 'host': _favorites_db_host()},
                status=status.HTTP_400_BAD_REQUEST
            )
        finally:
            for p in temp_dir.glob('*'):
                try:
                    p.unlink()
                except Exception:
                    pass
            try:
                temp_dir.rmdir()
            except Exception:
                pass
