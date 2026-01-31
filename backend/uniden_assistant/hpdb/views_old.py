from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.conf import settings
from pathlib import Path
from .models import (
    ScannerProfile, Frequency, ChannelGroup, Agency,
    Country, State, County, HPDBAgency, HPDBChannelGroup, HPDBFrequency,
    FavoritesList
)
from .serializers import (
    ScannerProfileSerializer, FrequencySerializer, ChannelGroupSerializer, AgencySerializer,
    CountrySerializer, StateSerializer, CountySerializer, 
    HPDBAgencySerializer, HPDBChannelGroupSerializer, HPDBFrequencySerializer,
    HPDBTreeSerializer, FavoritesListSerializer
)
from .parsers import UnidenFileParser
from .hpdb_parser import HPDBParser, FavoritesListParser
import tempfile


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
        return base_dir / 'ubcdx36' / 'favorites_lists'

    @action(detail=False, methods=['post'], url_path='export')
    def export_to_sd(self, request):
        favorites_dir = self._favorites_dir()
        favorites_dir.mkdir(parents=True, exist_ok=True)

        parser = UnidenFileParser()
        exported = 0
        errors = []

        for profile in ScannerProfile.objects.all():
            file_name = f"{profile.name.replace(' ', '_')}.hpd"
            file_path = favorites_dir / file_name
            try:
                content = parser.export(profile)
                file_path.write_text(content, encoding='utf-8')
                exported += 1
            except Exception as exc:
                errors.append({'profile': profile.name, 'error': str(exc)})

        return Response({'exported': exported, 'errors': errors})


# HPDB ViewSets
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
        country_id = self.request.query_params.get('country', None)
        if country_id:
            queryset = queryset.filter(country_id=country_id)
        return queryset


class CountyViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Counties"""
    queryset = County.objects.all()
    serializer_class = CountySerializer
    
    def get_queryset(self):
        queryset = County.objects.all()
        state_id = self.request.query_params.get('state', None)
        if state_id:
            queryset = queryset.filter(state_id=state_id)
        return queryset


class HPDBAgencyViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for HPDB Agencies"""
    queryset = HPDBAgency.objects.all()
    serializer_class = HPDBAgencySerializer
    
    def get_queryset(self):
        queryset = HPDBAgency.objects.all()
        state_id = self.request.query_params.get('state', None)
        county_id = self.request.query_params.get('county', None)
        
        if state_id:
            queryset = queryset.filter(states__state_id=state_id)
        if county_id:
            queryset = queryset.filter(counties__county_id=county_id)
        
        return queryset.distinct()


class HPDBChannelGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for HPDB Channel Groups"""
    queryset = HPDBChannelGroup.objects.all()
    serializer_class = HPDBChannelGroupSerializer
    
    def get_queryset(self):
        queryset = HPDBChannelGroup.objects.all()
        agency_id = self.request.query_params.get('agency', None)
        if agency_id:
            queryset = queryset.filter(agency_id=agency_id)
        return queryset


class HPDBFrequencyViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for HPDB Frequencies"""
    queryset = HPDBFrequency.objects.all()
    serializer_class = HPDBFrequencySerializer
    
    def get_queryset(self):
        queryset = HPDBFrequency.objects.all()
        cgroup_id = self.request.query_params.get('cgroup', None)
        if cgroup_id:
            queryset = queryset.filter(cgroup_id=cgroup_id)
        return queryset


class HPDBTreeViewSet(viewsets.ViewSet):
    """ViewSet for HPDB hierarchical tree view"""
    
    @action(detail=False, methods=['get'], url_path='tree')
    def tree(self, request):
        """Get hierarchical tree: Country > [Nationwide] > State > [Statewide] > County > [County Systems] > Agency
        Note: Channel groups are NOT included in tree to avoid performance issues - they're lazy-loaded via separate API"""
        tree = []
        
        # Get the _MultipleStates state for nationwide agencies
        multistate = State.objects.filter(name='_MultipleStates').first()
        
        for country in Country.objects.all():
            country_node = {
                'id': f'country-{country.id}',
                'type': 'country',
                'name': country.name,
                'code': country.code,
                'children': []
            }
            
            # Add Nationwide category at country level (if we have nationwide agencies)
            nationwide_agencies = []
            if multistate:
                nationwide_agencies = list(HPDBAgency.objects.filter(
                    states=multistate, 
                    counties__isnull=True
                ).distinct())
            
            if nationwide_agencies:
                nationwide_node = {
                    'id': f'category-nationwide-{country.id}',
                    'type': 'category',
                    'name': 'Nationwide',
                    'children': []
                }
                for agency in nationwide_agencies:
                    agency_node = {
                        'id': f'agency-{agency.id}',
                        'type': 'agency',
                        'name': agency.name,
                        'agency_id': agency.agency_id,
                        'system_type': agency.system_type,
                        'enabled': agency.enabled,
                        'group_count': agency.channel_groups.count()
                    }
                    nationwide_node['children'].append(agency_node)
                country_node['children'].append(nationwide_node)
            
            # Add states
            for state in country.states.all():
                # Skip _MultipleStates in the tree, we already used its agencies for "Nationwide"
                if state.name == '_MultipleStates':
                    continue
                    
                state_node = {
                    'id': f'state-{state.id}',
                    'type': 'state',
                    'name': state.name,
                    'code': state.code,
                    'state_id': state.state_id,
                    'children': []
                }
                
                # Add Statewide category at state level (if there are statewide agencies)
                statewide_agencies = list(HPDBAgency.objects.filter(
                    states=state, 
                    counties__isnull=True
                ).distinct())
                
                if statewide_agencies:
                    statewide_node = {
                        'id': f'category-statewide-{state.id}',
                        'type': 'category',
                        'name': 'Statewide',
                        'children': []
                    }
                    for agency in statewide_agencies:
                        agency_node = {
                            'id': f'agency-{agency.id}',
                            'type': 'agency',
                            'name': agency.name,
                            'agency_id': agency.agency_id,
                            'system_type': agency.system_type,
                            'enabled': agency.enabled,
                            'group_count': agency.channel_groups.count()
                        }
                        statewide_node['children'].append(agency_node)
                    state_node['children'].append(statewide_node)
                
                # Add counties with only their county-specific agencies
                for county in state.counties.all():
                    # Get county-specific agencies
                    county_agencies = list(HPDBAgency.objects.filter(counties=county).distinct())
                    
                    # Only add county if it has agencies
                    if county_agencies:
                        county_node = {
                            'id': f'county-{county.id}',
                            'type': 'county',
                            'name': county.name,
                            'county_id': county.county_id,
                            'children': []
                        }
                        
                        # Create County Systems category
                        county_systems_node = {
                            'id': f'category-county-{county.id}',
                            'type': 'category',
                            'name': 'County Systems',
                            'children': []
                        }
                        for agency in county_agencies:
                            agency_node = {
                                'id': f'agency-{agency.id}',
                                'type': 'agency',
                                'name': agency.name,
                                'agency_id': agency.agency_id,
                                'system_type': agency.system_type,
                                'enabled': agency.enabled,
                                'group_count': agency.channel_groups.count()
                            }
                            county_systems_node['children'].append(agency_node)
                        county_node['children'].append(county_systems_node)
                        state_node['children'].append(county_node)
                
                if state_node['children']:  # Only add state if it has data
                    country_node['children'].append(state_node)
            
            if country_node['children']:  # Only add country if it has data
                tree.append(country_node)
        
        return Response(tree)


class HPDBImportViewSet(viewsets.ViewSet):
    """Import HPDB data from uploaded files"""

    def create(self, request):
        files = request.FILES.getlist('files')
        if not files:
            return Response({'error': 'No files uploaded.'}, status=status.HTTP_400_BAD_REQUEST)

        filenames = [f.name.lower() for f in files]
        if 'hpdb.cfg' not in filenames:
            return Response({'error': 'Missing hpdb.cfg.'}, status=status.HTTP_400_BAD_REQUEST)
        if not any(name.startswith('s_') and name.endswith('.hpd') for name in filenames):
            return Response({'error': 'Missing s_*.hpd system files.'}, status=status.HTTP_400_BAD_REQUEST)

        temp_dir = Path(tempfile.mkdtemp(prefix='uniden_hpdb_'))
        try:
            saved = {}
            for f in files:
                target = temp_dir / f.name
                with open(target, 'wb') as out:
                    for chunk in f.chunks():
                        out.write(chunk)
                saved[f.name.lower()] = target

            parser = HPDBParser()
            parser.parse_hpdb_cfg(str(saved['hpdb.cfg']))

            system_files = [p for n, p in saved.items() if n.startswith('s_') and n.endswith('.hpd')]
            imported = 0
            errors = []
            for path in sorted(system_files):
                try:
                    parser.parse_system_file(str(path))
                    imported += 1
                except Exception as exc:
                    errors.append({'file': path.name, 'error': str(exc)})

            return Response({
                'imported': imported,
                'errors': errors
            })
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


class FavoritesListViewSet(viewsets.ModelViewSet):
    """ViewSet for Favorites Lists"""
    queryset = FavoritesList.objects.all()
    serializer_class = FavoritesListSerializer
    
    @action(detail=True, methods=['get'], url_path='detail')
    def favorite_detail(self, request, pk=None):
        """Get detailed channel information from favorite's .hpd file"""
        favorite = self.get_object()
        
        # Load the .hpd file for this favorite
        favorites_dir = Path(settings.UNIDEN_DATA_DIR).expanduser().resolve() / 'uniden' / 'ubcdx36' / 'favorites_lists'
        hpd_file = favorites_dir / favorite.filename
        
        if not hpd_file.exists():
            return Response({'error': f'File not found: {favorite.filename}'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            parser = UnidenFileParser()
            # Parse the file and extract channel groups and frequencies
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
                    
                    if record_type == 'Conventional' or record_type == 'Trunk':
                        # Parse agency/conventional info
                        pass
                    elif record_type == 'C-Group':
                        # Parse channel group
                        # Format: C-Group<tab><empty><tab><empty><tab><name><tab>On/Off<tab>...
                        try:
                            name = ''
                            # Skip empty parts and find the first non-empty one
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
                        # Parse frequency - works even without current_group
                        # Format: C-Freq<tab><empty><tab><empty><tab><name><tab>On/Off<tab><frequency><tab><modulation><tab>...
                        try:
                            freq_name = ''
                            frequency = None
                            modulation = ''
                            
                            # Find the name (first non-empty field that's not On/Off)
                            for i in range(1, min(6, len(parts))):
                                if parts[i].strip() and parts[i].strip() not in ['On', 'Off']:
                                    freq_name = parts[i].strip()
                                    break
                            
                            # Frequency is typically in parts[5]
                            if len(parts) > 5:
                                freq_str = parts[5].strip()
                                if freq_str.isdigit():
                                    frequency = int(freq_str)
                            
                            # Modulation is typically in parts[6]
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
                                
                                # Add to current group if exists, otherwise create default group
                                if current_group:
                                    current_group['frequencies'].append(freq_entry)
                                else:
                                    # Create a default group if no group was defined
                                    if not groups:
                                        current_group = {'id': group_counter, 'name': 'Default Group', 'frequencies': []}
                                        groups.append(current_group)
                                        group_counter += 1
                                    else:
                                        current_group = groups[0]
                                    current_group['frequencies'].append(freq_entry)
                        except (ValueError, IndexError) as e:
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

        filenames = [f.name.lower() for f in files]
        if 'f_list.cfg' not in filenames:
            return Response({'error': 'Missing f_list.cfg.'}, status=status.HTTP_400_BAD_REQUEST)
        if not any(name.endswith('.hpd') for name in filenames):
            return Response({'error': 'Missing .hpd files.'}, status=status.HTTP_400_BAD_REQUEST)

        temp_dir = Path(tempfile.mkdtemp(prefix='uniden_favorites_'))
        try:
            # Save all uploaded files
            saved = {}
            for f in files:
                target = temp_dir / f.name
                with open(target, 'wb') as out:
                    for chunk in f.chunks():
                        out.write(chunk)
                saved[f.name.lower()] = target

            # Parse favorites list cfg
            FavoritesListParser.parse_favorites_list(str(saved['f_list.cfg']))

            # Import profiles from .hpd files
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
        finally:
            # Best-effort cleanup
            for p in temp_dir.glob('*'):
                try:
                    p.unlink()
                except Exception:
                    pass
            try:
                temp_dir.rmdir()
            except Exception:
                pass
