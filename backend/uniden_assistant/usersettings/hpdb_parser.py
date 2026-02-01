"""Parser for HPDB database files from ubcdx36/HPDB folder"""
import os
import logging
from typing import Dict, List, Optional
from .models import Country, State, County, HPDBAgency, HPDBChannelGroup, HPDBFrequency, ScannerFileRecord

logger = logging.getLogger(__name__)


class HPDBParser:
    """Parser for hpdb.cfg and s_*.hpd files"""
    
    def __init__(self):
        self.countries: Dict[int, Country] = {}
        self.states: Dict[int, State] = {}
        self.counties: Dict[int, County] = {}
    
    def parse_hpdb_cfg(self, file_path: str):
        """Parse hpdb.cfg file to extract state and county information"""
        logger.info(f"Parsing HPDB config: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split('\t')
                if len(parts) < 2:
                    continue
                
                record_type = parts[0]
                
                if record_type == 'StateInfo':
                    self._parse_state_info(parts)
                elif record_type == 'CountyInfo':
                    self._parse_county_info(parts)
        
        logger.info(f"Parsed {len(self.states)} states and {len(self.counties)} counties")

    def parse_directory(self, directory: str, limit: Optional[int] = None) -> Dict[str, int]:
        """Parse an HPDB directory containing hpdb.cfg and s_*.hpd files."""
        hpdb_cfg = os.path.join(directory, 'hpdb.cfg')
        if not os.path.exists(hpdb_cfg):
            raise FileNotFoundError(f"hpdb.cfg not found: {hpdb_cfg}")

        self.parse_hpdb_cfg(hpdb_cfg)

        system_files = [
            os.path.join(directory, f)
            for f in os.listdir(directory)
            if f.startswith('s_') and f.endswith('.hpd')
        ]
        system_files.sort()

        if limit:
            system_files = system_files[:limit]

        for file_path in system_files:
            self.parse_system_file(file_path)

        return {
            'states': len(self.states),
            'counties': len(self.counties),
            'systems': len(system_files),
        }
    
    def _parse_state_info(self, parts: List[str]):
        """Parse StateInfo line from hpdb.cfg"""
        # Format: StateInfo\tStateId=X\tCountryId=Y\tName\tCode
        if len(parts) < 4:
            return
        
        try:
            state_id_str = parts[1].split('=')[1]
            country_id_str = parts[2].split('=')[1]
            
            state_id = int(state_id_str)
            country_id = int(country_id_str)
            name = parts[3] if len(parts) > 3 else ''
            code = parts[4] if len(parts) > 4 else ''
            
            # Skip StateId=0 (used for _MultipleStates)
            if state_id == 0:
                return
            
            # Create or get country
            if country_id not in self.countries:
                country_name = 'USA' if country_id == 1 else 'Canada' if country_id == 2 else f'Country {country_id}'
                country, _ = Country.objects.get_or_create(
                    country_id=country_id,
                    defaults={'name': country_name}
                )
                self.countries[country_id] = country
            
            # Create state
            state, created = State.objects.get_or_create(
                state_id=state_id,
                defaults={
                    'country': self.countries[country_id],
                    'name': name,
                    'code': code
                }
            )
            self.states[state_id] = state
            
            if created:
                logger.debug(f"Created state: {name} ({code})")
        
        except (IndexError, ValueError) as e:
            logger.warning(f"Error parsing StateInfo: {parts} - {e}")
    
    def _parse_county_info(self, parts: List[str]):
        """Parse CountyInfo line from hpdb.cfg"""
        # Format: CountyInfo\tCountyId=X\tStateId=Y\tName
        if len(parts) < 4:
            return
        
        try:
            county_id = int(parts[1].split('=')[1])
            state_id = int(parts[2].split('=')[1])
            name = parts[3]
            
            if state_id not in self.states:
                logger.warning(f"State {state_id} not found for county {name}")
                return
            
            county, created = County.objects.get_or_create(
                county_id=county_id,
                defaults={
                    'state': self.states[state_id],
                    'name': name
                }
            )
            self.counties[county_id] = county
            
            if created:
                logger.debug(f"Created county: {name}")
        
        except (IndexError, ValueError) as e:
            logger.warning(f"Error parsing CountyInfo: {parts} - {e}")
    
    def parse_system_file(self, file_path: str):
        """Parse a single s_*.hpd file containing system data"""
        logger.info(f"Parsing HPDB system file: {file_path}")
        
        current_agency = None
        current_group = None
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split('\t')
                if len(parts) < 2:
                    continue
                
                record_type = parts[0]
                
                if record_type == 'Conventional' or record_type == 'Trunk':
                    current_agency = self._parse_agency(parts, record_type)
                    current_group = None
                elif record_type == 'AreaState' and current_agency:
                    self._parse_area_state(parts, current_agency)
                elif record_type == 'AreaCounty' and current_agency:
                    self._parse_area_county(parts, current_agency)
                elif record_type == 'C-Group' and current_agency:
                    current_group = self._parse_channel_group(parts, current_agency)
                elif record_type == 'C-Freq' and current_group:
                    self._parse_frequency(parts, current_group)
        
        logger.info(f"Completed parsing {file_path}")
    
    def _parse_agency(self, parts: List[str], system_type: str) -> Optional[HPDBAgency]:
        """Parse Conventional or Trunk agency line"""
        # Format: Conventional\tAgencyId=X\tStateId=Y\tName\tOn/Off\t...
        try:
            agency_id = None
            state_id = None
            name = ''
            enabled = False
            
            for i, part in enumerate(parts):
                if part.startswith('AgencyId='):
                    agency_id = int(part.split('=')[1])
                elif part.startswith('StateId='):
                    state_id = int(part.split('=')[1])
                elif i >= 2 and not '=' in part and part not in ['Conventional', 'Trunk']:
                    if not name:
                        name = part
                    elif part in ['On', 'Off']:
                        enabled = (part == 'On')
            
            if agency_id is None or not name:
                return None
            
            agency, created = HPDBAgency.objects.get_or_create(
                agency_id=agency_id,
                defaults={
                    'name': name,
                    'system_type': system_type,
                    'enabled': enabled
                }
            )
            
            if created:
                logger.debug(f"Created agency: {name} ({system_type})")
            
            return agency
        
        except (IndexError, ValueError) as e:
            logger.warning(f"Error parsing agency: {parts} - {e}")
            return None
    
    def _parse_area_state(self, parts: List[str], agency: HPDBAgency):
        """Parse AreaState line to link agency to states"""
        # Format: AreaState\tAgencyId=X\tStateId=Y
        try:
            state_id = None
            for part in parts:
                if part.startswith('StateId='):
                    state_id = int(part.split('=')[1])
            
            if state_id and state_id != 0 and state_id in self.states:
                agency.states.add(self.states[state_id])
        
        except (IndexError, ValueError) as e:
            logger.warning(f"Error parsing AreaState: {parts} - {e}")
    
    def _parse_area_county(self, parts: List[str], agency: HPDBAgency):
        """Parse AreaCounty line to link agency to counties"""
        # Format: AreaCounty\tAgencyId=X\tCountyId=Y
        # Note: CountyId=0 means statewide/nationwide (not specific to a county)
        try:
            county_id = None
            for part in parts:
                if part.startswith('CountyId='):
                    county_id = int(part.split('=')[1])
            
            # Only add to specific counties if CountyId is not 0
            # CountyId=0 means "statewide" or "nationwide" - these appear under the state node
            if county_id and county_id != 0 and county_id in self.counties:
                agency.counties.add(self.counties[county_id])
            # If CountyId=0, the agency will appear under the state (via the states relationship)
        
        except (IndexError, ValueError) as e:
            logger.warning(f"Error parsing AreaCounty: {parts} - {e}")
    
    def _parse_channel_group(self, parts: List[str], agency: HPDBAgency) -> Optional[HPDBChannelGroup]:
        """Parse C-Group line"""
        # Format: C-Group\tCGroupId=X\tAgencyId=Y\tName\tOn/Off\tLat\tLon\tRange\tType
        try:
            cgroup_id = None
            name = ''
            enabled = False
            latitude = None
            longitude = None
            range_miles = None
            location_type = ''
            
            for i, part in enumerate(parts):
                if part.startswith('CGroupId='):
                    cgroup_id = int(part.split('=')[1])
                elif i >= 3 and not '=' in part and part not in ['C-Group', 'On', 'Off']:
                    if not name:
                        name = part
                    elif part in ['On', 'Off']:
                        enabled = (part == 'On')
                    elif not location_type and part in ['Circle', 'Rectangles']:
                        location_type = part
            
            # Try to extract numeric values
            for part in parts[4:]:
                if '=' not in part:
                    try:
                        val = float(part)
                        if latitude is None and -90 <= val <= 90:
                            latitude = val
                        elif longitude is None and -180 <= val <= 180:
                            longitude = val
                        elif range_miles is None and val > 0:
                            range_miles = val
                    except ValueError:
                        pass
            
            if cgroup_id is None:
                return None
            
            group, created = HPDBChannelGroup.objects.get_or_create(
                cgroup_id=cgroup_id,
                agency=agency,
                defaults={
                    'name': name,
                    'enabled': enabled,
                    'latitude': latitude,
                    'longitude': longitude,
                    'range_miles': range_miles,
                    'location_type': location_type
                }
            )
            
            if created:
                logger.debug(f"Created channel group: {name}")
            
            return group
        
        except (IndexError, ValueError) as e:
            logger.warning(f"Error parsing channel group: {parts} - {e}")
            return None
    
    def _parse_frequency(self, parts: List[str], group: HPDBChannelGroup):
        """Parse C-Freq line"""
        # Format: C-Freq\tCFreqId=X\tCGroupId=Y\tName\tOn/Off\tFrequency\tModulation\tTone\tDelay
        try:
            cfreq_id = None
            name = ''
            enabled = False
            frequency = None
            modulation = ''
            tone = ''
            delay = 15
            
            for i, part in enumerate(parts):
                if part.startswith('CFreqId='):
                    cfreq_id = int(part.split('=')[1])
                elif i >= 3 and not '=' in part:
                    if not name and part not in ['C-Freq', 'On', 'Off']:
                        name = part
                    elif part in ['On', 'Off']:
                        enabled = (part == 'On')
                    elif part.isdigit() and frequency is None:
                        frequency = int(part)
                    elif part in ['AM', 'FM', 'NFM', 'AUTO'] and not modulation:
                        modulation = part
                    elif part.startswith('TONE=') or part.startswith('NAC='):
                        tone = part
                    elif part.isdigit() and frequency is not None:
                        delay = int(part)
            
            if cfreq_id is None or frequency is None:
                return
            
            freq, created = HPDBFrequency.objects.get_or_create(
                cfreq_id=cfreq_id,
                cgroup=group,
                defaults={
                    'name': name,
                    'enabled': enabled,
                    'frequency': frequency,
                    'modulation': modulation,
                    'tone': tone,
                    'delay': delay
                }
            )
            
            if created:
                logger.debug(f"Created frequency: {name} - {frequency/1000000:.4f} MHz")
        
        except (IndexError, ValueError) as e:
            logger.warning(f"Error parsing frequency: {parts} - {e}")


class FavoritesListParser:
    """Parser for f_list.cfg file"""
    
    @staticmethod
    def parse_favorites_list(file_path: str):
        """Parse f_list.cfg file"""
        from .models import FavoritesList
        import json
        
        logger.info(f"Parsing favorites list: {file_path}")
        
        FavoritesList.objects.all().delete()  # Clear existing

        records_buffer = []
        order = 0
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_number, raw_line in enumerate(f, start=1):
                raw_line = raw_line.rstrip('\n').rstrip('\r')
                if raw_line:
                    trailing_empty = len(raw_line) - len(raw_line.rstrip('\t'))
                    parts_all = raw_line.split('\t')
                    record_type = parts_all[0] if parts_all else ''
                    fields = parts_all[1:] if len(parts_all) > 1 else []

                    records_buffer.append(ScannerFileRecord(
                        file_name=os.path.basename(file_path),
                        file_path='favorites_lists/f_list.cfg',
                        record_type=record_type,
                        fields=fields,
                        trailing_empty_fields=trailing_empty,
                        line_number=line_number,
                    ))

                    if len(records_buffer) >= 2000:
                        ScannerFileRecord.objects.bulk_create(records_buffer)
                        records_buffer.clear()

                line = raw_line.strip()
                if not line or line.startswith('TargetModel') or line.startswith('FormatVersion'):
                    continue
                
                parts = line.split('\t')
                if len(parts) < 7:
                    continue
                
                # Check for F-List record (may have trailing space in first column)
                if not parts[0].strip().startswith('F-List'):
                    continue
                
                try:
                    name = parts[1].strip() if len(parts) > 1 else ''
                    filename = parts[2].strip() if len(parts) > 2 else ''
                    enabled = (parts[3].strip() == 'On') if len(parts) > 3 else False
                    disabled_on_power = (parts[4].strip() == 'On') if len(parts) > 4 else False
                    quick_key = parts[5].strip() if len(parts) > 5 else ''
                    list_number = int(parts[6].strip()) if len(parts) > 6 and parts[6].strip().isdigit() else 0
                    
                    # Store all remaining flags
                    flags = [p.strip() for p in parts[7:]] if len(parts) > 7 else []
                    flags_json = json.dumps(flags)
                    
                    FavoritesList.objects.create(
                        name=name,
                        filename=filename,
                        enabled=enabled,
                        disabled_on_power=disabled_on_power,
                        quick_key=quick_key,
                        list_number=list_number,
                        order=order,
                        flags=flags_json,
                        raw_data=line
                    )
                    
                    order += 1
                    logger.debug(f"Created favorites list: {name} ({filename})")
                
                except (IndexError, ValueError) as e:
                    logger.warning(f"Error parsing favorites list: {parts} - {e}")
        
        if records_buffer:
            ScannerFileRecord.objects.bulk_create(records_buffer)

        logger.info(f"Parsed {order} favorites lists")
