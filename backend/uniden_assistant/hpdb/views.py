from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.utils import DatabaseError
import logging
from django.conf import settings
from pathlib import Path
from .models import (
    Country, State, County, HPDBAgency, HPDBChannelGroup, HPDBFrequency
)
from .serializers import (
    CountrySerializer, StateSerializer, CountySerializer, 
    HPDBAgencySerializer, HPDBChannelGroupSerializer, HPDBFrequencySerializer,
    HPDBTreeSerializer
)
from .hpdb_parser import HPDBParser
import tempfile

logger = logging.getLogger(__name__)


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
        """Get hierarchical tree: Country > [Nationwide] > State > [Statewide] > County > [County Systems] > Agency"""
        tree = []
        
        multistate = State.objects.filter(name='_MultipleStates').first()
        
        for country in Country.objects.all():
            country_node = {
                'id': f'country-{country.id}',
                'type': 'country',
                'name': country.name,
                'code': country.code,
                'children': []
            }
            
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
            
            for state in country.states.all():
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
                
                for county in state.counties.all():
                    county_agencies = list(HPDBAgency.objects.filter(counties=county).distinct())
                    
                    if county_agencies:
                        county_node = {
                            'id': f'county-{county.id}',
                            'type': 'county',
                            'name': county.name,
                            'county_id': county.county_id,
                            'children': []
                        }
                        
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
                
                if state_node['children']:
                    country_node['children'].append(state_node)
            
            if country_node['children']:
                tree.append(country_node)
        
        return Response(tree)


class HPDBImportViewSet(viewsets.ViewSet):
    """Import HPDB data from uploaded files"""

    def create(self, request):
        files = request.FILES.getlist('files')
        if not files:
            return Response({'error': 'No files uploaded.'}, status=status.HTTP_400_BAD_REQUEST)

        filenames = [Path(f.name).name.lower() for f in files]
        if 'hpdb.cfg' not in filenames:
            return Response({'error': 'Missing hpdb.cfg.'}, status=status.HTTP_400_BAD_REQUEST)
        if not any(name.startswith('s_') and name.endswith('.hpd') for name in filenames):
            return Response({'error': 'Missing s_*.hpd system files.'}, status=status.HTTP_400_BAD_REQUEST)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            for f in files:
                dest = tmppath / Path(f.name).name
                with dest.open('wb') as out:
                    for chunk in f.chunks():
                        out.write(chunk)

            parser = HPDBParser()
            try:
                result = parser.parse_directory(str(tmppath))
                return Response(result, status=status.HTTP_201_CREATED)
            except DatabaseError as e:
                logger.exception("HPDB import failed", exc_info=e)
                return Response(
                    {'error': str(e), 'host': _hpdb_db_host()},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
