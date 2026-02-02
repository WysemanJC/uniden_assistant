from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.utils import DatabaseError
import logging
from django.shortcuts import get_object_or_404
from django.conf import settings
from pathlib import Path
from django.http import HttpResponse
import io
import zipfile
from .models import (
    ScannerProfile, Frequency, ChannelGroup, Agency, FavoritesList, ScannerRawFile, ScannerRawLine,
    ConventionalSystem, TrunkSystem, CGroup, CFreq, Site, BandPlanP25, BandPlanMot, TFreq, TGroup,
    TGID, Rectangle, FleetMap, UnitId, AvoidTgid
)
from .serializers import (
    ScannerProfileSerializer, FrequencySerializer, ChannelGroupSerializer, 
    AgencySerializer, FavoritesListSerializer, FavoritesListDetailSerializer
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


class ClearUserSettingsDataView(APIView):
    """Clear all user settings and favourites data"""

    def post(self, request):
        try:
            logger.info("Clearing all user settings and favourites data")
            
            # Clear all data from favorites database
            ScannerProfile.objects.using('favorites').all().delete()
            Frequency.objects.using('favorites').all().delete()
            ChannelGroup.objects.using('favorites').all().delete()
            Agency.objects.using('favorites').all().delete()
            FavoritesList.objects.using('favorites').all().delete()
            ConventionalSystem.objects.using('favorites').all().delete()
            TrunkSystem.objects.using('favorites').all().delete()
            CGroup.objects.using('favorites').all().delete()
            CFreq.objects.using('favorites').all().delete()
            Site.objects.using('favorites').all().delete()
            BandPlanP25.objects.using('favorites').all().delete()
            BandPlanMot.objects.using('favorites').all().delete()
            TFreq.objects.using('favorites').all().delete()
            TGroup.objects.using('favorites').all().delete()
            TGID.objects.using('favorites').all().delete()
            Rectangle.objects.using('favorites').all().delete()
            FleetMap.objects.using('favorites').all().delete()
            UnitId.objects.using('favorites').all().delete()
            AvoidTgid.objects.using('favorites').all().delete()
            
            logger.info("Cleared all user settings and favourites data successfully")
            return Response({'success': True, 'message': 'All user settings and favourites data cleared'})
        except DatabaseError as e:
            logger.exception("Failed to clear user settings data", exc_info=e)
            return Response(
                {'error': f'Failed to clear data: {str(e)}', 'host': _favorites_db_host()},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.exception("Failed to clear user settings data", exc_info=e)
            return Response(
                {'error': f'Failed to clear data: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ClearScannerRawDataView(APIView):
    """Clear all raw scanner file data from the database"""

    def post(self, request):
        try:
            logger.info("Clearing scanner raw data")
            # Delete raw files and lines (cascades to lines automatically)
            ScannerRawFile.objects.using('favorites').all().delete()
            
            logger.info("Scanner raw data cleared successfully")
            return Response({'message': 'Scanner raw data cleared successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Failed to clear scanner raw data", exc_info=e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ExportFavoritesFolderView(APIView):
    """Export all favorites lists to a zip file containing favorites_lists directory."""

    def get(self, request):
        try:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                f_list_content = self._build_f_list_cfg()
                zip_file.writestr('favorites_lists/f_list.cfg', f_list_content)

                favorites_lists = FavoritesList.objects.using('favorites').all().order_by('order', 'filename')
                for favorites_list in favorites_lists:
                    hpd_content = self._build_favorites_hpd(favorites_list)
                    zip_file.writestr(f"favorites_lists/{favorites_list.filename}", hpd_content)

            zip_buffer.seek(0)
            response = HttpResponse(zip_buffer.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="favorites_lists_export.zip"'
            return response
        except Exception as exc:
            logger.exception("Failed to export favorites folder", exc_info=exc)
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _build_f_list_cfg(self) -> str:
        favorites_lists = FavoritesList.objects.using('favorites').all().order_by('order', 'filename')
        scanner_model = favorites_lists[0].scanner_model if favorites_lists else 'BCDx36HP'
        format_version = favorites_lists[0].format_version if favorites_lists else '1.00'

        lines = [
            self._join_record('TargetModel', [scanner_model]),
            self._join_record('FormatVersion', [format_version]),
        ]

        for fav in favorites_lists:
            startup_keys = self._pad_list(fav.startup_keys, 10, 'Off')
            s_qkeys = self._pad_list(fav.s_qkeys, 100, 'Off')
            fields = [
                fav.user_name or '',
                fav.filename or '',
                fav.location_control or 'Off',
                fav.monitor or 'Off',
                fav.quick_key or 'Off',
                fav.number_tag or 'Off',
                *startup_keys,
                *s_qkeys,
            ]
            lines.append(self._join_record('F-List ', fields))

        return '\n'.join(lines) + '\n'

    def _build_favorites_hpd(self, favorites_list: FavoritesList) -> str:
        lines = [
            self._join_record('TargetModel', [favorites_list.scanner_model or 'BCDx36HP']),
            self._join_record('FormatVersion', [favorites_list.format_version or '1.00']),
        ]

        conventional_systems = favorites_list.conventional_systems.using('favorites').all().order_by('order')
        for system in conventional_systems:
            lines.append(self._join_record('Conventional', [
                system.my_id or '',
                system.parent_id or '',
                system.name_tag or '',
                system.avoid or 'Off',
                system.reserve or '',
                system.system_type or '',
                system.quick_key or 'Off',
                system.number_tag or 'Off',
                str(system.system_hold_time),
                system.analog_agc or 'Off',
                system.digital_agc or 'Off',
                str(system.digital_waiting_time),
                system.digital_threshold_mode or 'Manual',
                str(system.digital_threshold_level),
            ]))

            dqks_flags = self._pad_list(system.dqks_status, 100, 'Off')
            lines.append(self._join_record('DQKs_Status', [system.dqks_my_id or '', *dqks_flags]))

            cgroups = system.cgroups.using('favorites').all().order_by('order')
            for group in cgroups:
                lines.append(self._join_record('C-Group', [
                    group.my_id or '',
                    group.parent_id or '',
                    group.name_tag or '',
                    group.avoid or 'Off',
                    self._format_decimal(group.latitude, 6),
                    self._format_decimal(group.longitude, 6),
                    self._format_decimal(group.range_miles, 1),
                    group.location_type or 'Circle',
                    group.quick_key or 'Off',
                    group.filter or '',
                ]))

                cfreqs = group.cfreqs.using('favorites').all().order_by('order')
                for cfreq in cfreqs:
                    lines.append(self._join_record('C-Freq', [
                        cfreq.my_id or '',
                        cfreq.parent_id or '',
                        cfreq.name_tag or '',
                        cfreq.avoid or 'Off',
                        str(cfreq.frequency),
                        cfreq.modulation or 'AUTO',
                        cfreq.audio_option or '',
                        str(cfreq.func_tag_id),
                        cfreq.attenuator or 'Off',
                        str(cfreq.delay),
                        str(cfreq.volume_offset),
                        cfreq.alert_tone or 'Off',
                        cfreq.alert_volume or 'Auto',
                        cfreq.alert_color or 'Off',
                        cfreq.alert_pattern or 'On',
                        cfreq.number_tag or 'Off',
                        cfreq.priority_channel or 'Off',
                    ]))

                rectangles = group.rectangles.using('favorites').all().order_by('order')
                for rect in rectangles:
                    lines.append(self._join_record('Rectangle', [
                        rect.my_id or '',
                        self._format_decimal(rect.latitude1, 6),
                        self._format_decimal(rect.longitude1, 6),
                        self._format_decimal(rect.latitude2, 6),
                        self._format_decimal(rect.longitude2, 6),
                    ]))

        trunk_systems = favorites_list.trunk_systems.using('favorites').all().order_by('order')
        for system in trunk_systems:
            lines.append(self._join_record('Trunk', [
                system.my_id or '',
                system.parent_id or '',
                system.name_tag or '',
                system.avoid or 'Off',
                system.reserve or '',
                system.system_type or '',
                system.id_search or 'Off',
                system.alert_tone or 'Off',
                system.alert_volume or 'Auto',
                system.status_bit or 'Ignore',
                system.nac or 'Srch',
                system.quick_key or 'Off',
                system.number_tag or 'Off',
                str(system.site_hold_time),
                system.analog_agc or 'Off',
                system.digital_agc or 'Off',
                system.end_code or 'Analog',
                system.priority_id_scan or 'Off',
                system.alert_color or 'Off',
                system.alert_pattern or 'On',
                system.tgid_format or '',
            ]))

            dqks_flags = self._pad_list(system.dqks_status, 100, 'Off')
            lines.append(self._join_record('DQKs_Status', [system.dqks_my_id or '', *dqks_flags]))

            fleet_maps = system.fleet_maps.using('favorites').all().order_by('order')
            for fleet in fleet_maps:
                blocks = self._pad_list(fleet.blocks, 8, '0')
                lines.append(self._join_record('FleetMap', [fleet.my_id or '', *blocks]))

            unit_ids = system.unit_ids.using('favorites').all().order_by('order')
            for unit in unit_ids:
                lines.append(self._join_record('UnitIds', [
                    unit.reserve1 or '',
                    unit.reserve2 or '',
                    unit.name_tag or '',
                    str(unit.unit_id),
                    unit.alert_tone or 'Off',
                    unit.alert_volume or 'Auto',
                    unit.alert_color or 'Off',
                    unit.alert_pattern or 'On',
                ]))

            avoid_tgids = system.avoid_tgids.using('favorites').all().order_by('order')
            for avoid in avoid_tgids:
                lines.append(self._join_record('AvoidTgids', [avoid.my_id or '', *avoid.tgids]))

            sites = system.sites.using('favorites').all().order_by('order')
            for site in sites:
                lines.append(self._join_record('Site', [
                    site.my_id or '',
                    site.parent_id or '',
                    site.name_tag or '',
                    site.avoid or 'Off',
                    self._format_decimal(site.latitude, 6),
                    self._format_decimal(site.longitude, 6),
                    self._format_decimal(site.range_miles, 1),
                    site.modulation or 'AUTO',
                    site.mot_band_type or 'Standard',
                    site.edacs_band_type or 'Wide',
                    site.location_type or 'Circle',
                    site.attenuator or 'Off',
                    str(site.digital_waiting_time),
                    site.digital_threshold_mode or 'Manual',
                    str(site.digital_threshold_level),
                    site.quick_key or 'Off',
                    site.nac or 'Srch',
                    site.filter or '',
                ]))

                if hasattr(site, 'bandplan_p25') and site.bandplan_p25:
                    lines.append(self._join_record('BandPlan_P25', self._format_bandplan_p25(site.bandplan_p25)))
                if hasattr(site, 'bandplan_mot') and site.bandplan_mot:
                    lines.append(self._join_record('BandPlan_Mot', self._format_bandplan_mot(site.bandplan_mot)))

                tfreqs = site.tfreqs.using('favorites').all().order_by('order')
                for tfreq in tfreqs:
                    lines.append(self._join_record('T-Freq', [
                        tfreq.reserve_my_id or '',
                        tfreq.parent_id or '',
                        tfreq.reserve1 or '',
                        tfreq.reserve_avoid or 'Off',
                        str(tfreq.frequency),
                        str(tfreq.lcn),
                        tfreq.color_code_ran_area or '',
                    ]))

                rectangles = site.rectangles.using('favorites').all().order_by('order')
                for rect in rectangles:
                    lines.append(self._join_record('Rectangle', [
                        rect.my_id or '',
                        self._format_decimal(rect.latitude1, 6),
                        self._format_decimal(rect.longitude1, 6),
                        self._format_decimal(rect.latitude2, 6),
                        self._format_decimal(rect.longitude2, 6),
                    ]))

            tgroups = system.tgroups.using('favorites').all().order_by('order')
            for tgroup in tgroups:
                lines.append(self._join_record('T-Group', [
                    tgroup.my_id or '',
                    tgroup.parent_id or '',
                    tgroup.name_tag or '',
                    tgroup.avoid or 'Off',
                    self._format_decimal(tgroup.latitude, 6),
                    self._format_decimal(tgroup.longitude, 6),
                    self._format_decimal(tgroup.range_miles, 1),
                    tgroup.location_type or 'Circle',
                    tgroup.quick_key or 'Off',
                ]))

                tgids = tgroup.tgids.using('favorites').all().order_by('order')
                for tgid in tgids:
                    lines.append(self._join_record('TGID', [
                        tgid.my_id or '',
                        tgid.parent_id or '',
                        tgid.name_tag or '',
                        tgid.avoid or 'Off',
                        tgid.tgid or '',
                        tgid.audio_type or 'ALL',
                        str(tgid.func_tag_id),
                        str(tgid.delay),
                        str(tgid.volume_offset),
                        tgid.alert_tone or 'Off',
                        tgid.alert_volume or 'Auto',
                        tgid.alert_color or 'Off',
                        tgid.alert_pattern or 'On',
                        tgid.number_tag or 'Off',
                        tgid.priority_channel or 'Off',
                        tgid.tdma_slot or 'Any',
                    ]))

                rectangles = tgroup.rectangles.using('favorites').all().order_by('order')
                for rect in rectangles:
                    lines.append(self._join_record('Rectangle', [
                        rect.my_id or '',
                        self._format_decimal(rect.latitude1, 6),
                        self._format_decimal(rect.longitude1, 6),
                        self._format_decimal(rect.latitude2, 6),
                        self._format_decimal(rect.longitude2, 6),
                    ]))

        return '\n'.join(lines) + '\n'

    @staticmethod
    def _join_record(record_type: str, fields: list[str]) -> str:
        sanitized = [str(f) if f is not None else '' for f in fields]
        if sanitized:
            return record_type + '\t' + '\t'.join(sanitized)
        return record_type

    @staticmethod
    def _pad_list(values: list, length: int, fill: str) -> list:
        values = list(values) if values else []
        if len(values) < length:
            values.extend([fill] * (length - len(values)))
        return values[:length]

    @staticmethod
    def _format_decimal(value, places: int) -> str:
        if value is None:
            return ''
        try:
            return f"{float(value):.{places}f}"
        except (ValueError, TypeError):
            return ''

    @staticmethod
    def _format_bandplan_p25(bandplan: BandPlanP25) -> list[str]:
        my_id = bandplan.site.my_id if bandplan.site else ''
        fields = [my_id]
        for idx in range(16):
            entry = bandplan.band_plan.get(str(idx), {}) if bandplan.band_plan else {}
            fields.append(str(entry.get('base', 0)))
            fields.append(str(entry.get('spacing', 0)))
        return fields

    @staticmethod
    def _format_bandplan_mot(bandplan: BandPlanMot) -> list[str]:
        my_id = bandplan.site.my_id if bandplan.site else ''
        fields = [my_id]
        for idx in range(6):
            entry = bandplan.band_plan.get(str(idx), {}) if bandplan.band_plan else {}
            fields.append(str(entry.get('lower', 0)))
            fields.append(str(entry.get('upper', 0)))
            fields.append(str(entry.get('spacing', 0)))
            fields.append(str(entry.get('offset', 0)))
        return fields


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
        # The serializer will handle the channel_group FK automatically
        # since it's provided in the request data
        serializer.save()


class ChannelGroupViewSet(viewsets.ModelViewSet):
    """ViewSet for Channel Groups"""
    serializer_class = ChannelGroupSerializer

    def get_queryset(self):
        profile_id = self.request.query_params.get('profile', None)
        if profile_id:
            return ChannelGroup.objects.filter(profile_id=profile_id)
        return ChannelGroup.objects.all()

    def perform_create(self, serializer):
        # Check if creating for a favorites list or a profile
        favorites_list_id = self.request.data.get('favorites_list')
        profile_id = self.request.data.get('profile')
        
        if favorites_list_id:
            favorites_list = get_object_or_404(FavoritesList, id=favorites_list_id)
            serializer.save(favorites_list=favorites_list)
        elif profile_id:
            profile = get_object_or_404(ScannerProfile, id=profile_id)
            serializer.save(profile=profile)
        else:
            # Must have one or the other
            raise ValidationError({'error': 'Either favorites_list or profile must be provided'})


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
    serializer_class = FavoritesListSerializer
    
    def get_queryset(self):
        return FavoritesList.objects.using('favorites').all()
    
    @action(detail=True, methods=['get'], url_path='detail')
    def favorite_detail(self, request, pk=None):
        """Get detailed information from favorite list including all systems and groups"""
        favorite = self.get_object()
        
        # Build groups list from conventional and trunk systems
        groups = []
        
        # Process conventional systems and their groups
        for conv_sys in favorite.conventional_systems.using('favorites').all().order_by('order'):
            for cgroup in conv_sys.cgroups.using('favorites').all().order_by('order'):
                # Count frequencies in this group
                freq_count = cgroup.cfreqs.using('favorites').count()
                groups.append({
                    'id': str(cgroup.id),
                    'name_tag': cgroup.name_tag,
                    'frequency_count': freq_count,
                    'freq_count': freq_count,
                    'system_type': 'Conventional',
                    'system_name': conv_sys.name_tag
                })
        
        # Process trunk systems and their groups (tgroups)
        for trunk_sys in favorite.trunk_systems.using('favorites').all().order_by('order'):
            for tgroup in trunk_sys.tgroups.using('favorites').all().order_by('order'):
                # Count TGIDs in this group
                tgid_count = tgroup.tgids.using('favorites').count()
                groups.append({
                    'id': str(tgroup.id),
                    'name_tag': tgroup.name_tag,
                    'frequency_count': tgid_count,
                    'freq_count': tgid_count,
                    'system_type': 'Trunked',
                    'system_name': trunk_sys.name_tag
                })
        
        return Response({
            'id': str(favorite.id),
            'user_name': favorite.user_name,
            'filename': favorite.filename,
            'scanner_model': favorite.scanner_model,
            'format_version': favorite.format_version,
            'favorites_list_id': str(favorite.id),
            'groups': groups,
            'total_groups': len(groups),
            'total_frequencies': sum(g['frequency_count'] for g in groups),
            'conventional_systems': len(favorite.conventional_systems.using('favorites').all()),
            'trunk_systems': len(favorite.trunk_systems.using('favorites').all())
        })


class FavoritesImportViewSet(viewsets.ViewSet):
    """Import favorites from uploaded files using new hierarchical structure"""

    def create(self, request):
        """Import favorites lists from f_list.cfg and f_*.hpd files"""
        from .favorites_hpd_parser import FavoritesHPDParser
        from .hpdb_parser import FavoritesListParser
        
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

            # Step 1: Parse f_list.cfg using FavoritesListParser
            if 'f_list.cfg' in saved:
                favorites_list_parser = FavoritesListParser()
                # Note: parse_favorites_list doesn't return anything but creates FavoritesList objects
                favorites_list_parser.parse_favorites_list(str(saved['f_list.cfg']))
                # Get the created FavoritesList objects
                f_list_count = FavoritesList.objects.using('favorites').count()
            else:
                return Response({'error': 'Failed to parse f_list.cfg'}, status=status.HTTP_400_BAD_REQUEST)

            # Step 2: Parse each f_*.hpd file using FavoritesHPDParser
            imported = 0
            errors = []
            
            for name, path in saved.items():
                if not name.endswith('.hpd'):
                    continue
                
                # Extract the filename (e.g., "f_000001.hpd")
                hpd_filename = path.name
                
                # Find the corresponding FavoritesList entry
                favorites_list = FavoritesList.objects.using('favorites').filter(filename=hpd_filename).first()
                if not favorites_list:
                    errors.append({'file': hpd_filename, 'error': 'No matching F-List entry found'})
                    continue
                
                try:
                    parser = FavoritesHPDParser()
                    parser.parse_file(str(path), favorites_list)
                    imported += 1
                    logger.info(f"Successfully imported {hpd_filename}")
                except Exception as exc:
                    logger.exception(f"Error parsing {hpd_filename}", exc_info=exc)
                    errors.append({'file': hpd_filename, 'error': str(exc)})

            return Response({
                'imported': imported,
                'errors': errors,
                'total_favorites_lists': f_list_count
            })
        except DatabaseError as exc:
            logger.exception("Favourites import failed", exc_info=exc)
            return Response(
                {'error': str(exc), 'host': _favorites_db_host()},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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


class CGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for CGroups (Conventional Groups) with their frequencies"""
    
    def get_queryset(self):
        return CGroup.objects.using('favorites').all()
    
    def retrieve(self, request, pk=None):
        """Get a CGroup with its frequencies"""
        try:
            cgroup = CGroup.objects.using('favorites').get(pk=pk)
            cfreqs = cgroup.cfreqs.using('favorites').all().order_by('order')
            
            frequencies = []
            for cfreq in cfreqs:
                frequencies.append({
                    'id': str(cfreq.id),
                    'name_tag': cfreq.name_tag,
                    'frequency': cfreq.frequency,
                    'modulation': cfreq.modulation,
                    'avoid': cfreq.avoid,
                    'audio_option': cfreq.audio_option,
                    'attenuator': cfreq.attenuator,
                    'delay': cfreq.delay,
                    'volume_offset': cfreq.volume_offset,
                    'alert_tone': cfreq.alert_tone,
                    'alert_volume': cfreq.alert_volume,
                    'alert_color': cfreq.alert_color,
                    'alert_pattern': cfreq.alert_pattern,
                    'number_tag': cfreq.number_tag,
                    'priority_channel': cfreq.priority_channel,
                    'order': cfreq.order
                })
            
            return Response({
                'id': str(cgroup.id),
                'name_tag': cgroup.name_tag,
                'frequencies': frequencies,
                'frequency_count': len(frequencies)
            })
        except CGroup.DoesNotExist:
            return Response({'error': 'CGroup not found'}, status=status.HTTP_404_NOT_FOUND)


class TGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for TGroups (Trunk Groups) with their TGIDs"""
    
    def get_queryset(self):
        return TGroup.objects.using('favorites').all()
    
    def retrieve(self, request, pk=None):
        """Get a TGroup with its TGIDs"""
        try:
            tgroup = TGroup.objects.using('favorites').get(pk=pk)
            tgids = tgroup.tgids.using('favorites').all().order_by('order')
            
            tgid_list = []
            for tgid in tgids:
                tgid_list.append({
                    'id': str(tgid.id),
                    'name_tag': tgid.name_tag,
                    'tgid': tgid.tgid,
                    'avoid': tgid.avoid,
                    'audio_type': tgid.audio_type,
                    'delay': tgid.delay,
                    'volume_offset': tgid.volume_offset,
                    'alert_tone': tgid.alert_tone,
                    'alert_volume': tgid.alert_volume,
                    'alert_color': tgid.alert_color,
                    'alert_pattern': tgid.alert_pattern,
                    'number_tag': tgid.number_tag,
                    'priority_channel': tgid.priority_channel,
                    'tdma_slot': tgid.tdma_slot,
                    'order': tgid.order
                })
            
            return Response({
                'id': str(tgroup.id),
                'name_tag': tgroup.name_tag,
                'tgids': tgid_list,
                'tgid_count': len(tgid_list)
            })
        except TGroup.DoesNotExist:
            return Response({'error': 'TGroup not found'}, status=status.HTTP_404_NOT_FOUND)
