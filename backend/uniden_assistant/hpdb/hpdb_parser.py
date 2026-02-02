"""Parser for HPDB database files from ubcdx36/HPDB folder"""
import os
import logging
from typing import Dict, List, Optional
from .models import Country, State, County, HPDBAgency, HPDBChannelGroup, HPDBFrequency, HPDBFileRecord, HPDBRawFile, HPDBRawLine, HPDBRectangle
from uniden_assistant.record_parser import RecordHandler, BaseRecordParser
from uniden_assistant.record_parser.spec_field_maps import build_spec_field_map

logger = logging.getLogger(__name__)


class HPDBParser:
    """Parser for hpdb.cfg and s_*.hpd files"""
    
    def __init__(self, progress_callback=None):
        self.countries: Dict[int, Country] = {}
        self.states: Dict[int, State] = {}
        self.counties: Dict[int, County] = {}
        self.agencies: Dict[int, HPDBAgency] = {}
        self.channel_groups: Dict[int, HPDBChannelGroup] = {}
        self.progress_callback = progress_callback
        self._current_agency = None
        self._current_group = None
        self._current_site_id = None
        self._hpdb_base_dir = None
        self._rectangles_cache: Dict[str, List[Dict]] = {}  # Cache rectangles by parent ID before saving
        
        # Initialize shared record handler
        self.record_handler = RecordHandler(using_db='hpdb')
        self._register_record_handlers()

        self._ensure_nationwide()
    
    def _register_record_handlers(self):
        """Register all record type handlers with the shared handler"""
        # Config records
        self.record_handler.register_handler('TargetModel', self._handle_target_model)
        self.record_handler.register_handler('FormatVersion', self._handle_format_version)
        self.record_handler.register_handler('DateModified', self._handle_date_modified)
        self.record_handler.register_handler('StateInfo', self._handle_state_info)
        self.record_handler.register_handler('CountyInfo', self._handle_county_info)
        
        # Conventional system records
        self.record_handler.register_handler('Conventional', self._handle_conventional)
        self.record_handler.register_handler('Trunk', self._handle_trunk)
        self.record_handler.register_handler('AreaState', self._handle_area_state)
        self.record_handler.register_handler('AreaCounty', self._handle_area_county)
        self.record_handler.register_handler('C-Group', self._handle_c_group)
        self.record_handler.register_handler('C-Freq', self._handle_c_freq)
        
        # Geographic coverage
        self.record_handler.register_handler('Rectangle', self._handle_rectangle)
        self.record_handler.register_handler('Circle', self._handle_circle)
        
        # Trunk system records
        self.record_handler.register_handler('Site', self._handle_site)
        self.record_handler.register_handler('T-Group', self._handle_t_group)
        self.record_handler.register_handler('T-Freq', self._handle_t_freq)
        self.record_handler.register_handler('TGID', self._handle_tgid)
        self.record_handler.register_handler('LM', self._handle_lm_site)
        self.record_handler.register_handler('LM_FREQUENCY', self._handle_lm_frequency)
        
        # Advanced features
        self.record_handler.register_handler('FleetMap', self._handle_fleet_map)
        self.record_handler.register_handler('UnitIds', self._handle_unit_ids)
        self.record_handler.register_handler('AvoidTgids', self._handle_avoid_tgids)
        self.record_handler.register_handler('BandPlan_Mot', self._handle_band_plan_mot)
        self.record_handler.register_handler('BandPlan_P25', self._handle_band_plan_p25)
        self.record_handler.register_handler('DQKs_Status', self._handle_dqks_status)

    def _ensure_nationwide(self):
        """Ensure special Nationwide country/state are available (CountryId=0, StateId=0)."""
        country = self.countries.get(0)
        if not country:
            country, _ = Country.objects.using('hpdb').update_or_create(
                country_id=0,
                defaults={'name_tag': 'Nationwide', 'code': ''}
            )
            self.countries[0] = country

        state = self.states.get(0)
        if not state:
            state, _ = State.objects.using('hpdb').update_or_create(
                state_id=0,
                defaults={'country': country, 'name_tag': 'Nationwide', 'short_name': ''}
            )
            self.states[0] = state
    
    def parse_hpdb_cfg(self, file_path: str):
        """Parse hpdb.cfg file to extract state and county information"""
        logger.info(f"Parsing HPDB config: {file_path}")

        if not self._hpdb_base_dir:
            self._hpdb_base_dir = os.path.dirname(file_path)

        self._store_raw_file(file_path)

        records_buffer: List[HPDBFileRecord] = []
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_number, raw_line in enumerate(f, start=1):
                raw_line = raw_line.rstrip('\n').rstrip('\r')
                if not raw_line:
                    continue

                record = self._build_file_record(raw_line, line_number, file_path)
                records_buffer.append(record)
                if len(records_buffer) >= 2000:
                    HPDBFileRecord.objects.bulk_create(records_buffer)
                    records_buffer.clear()

                line = raw_line.strip()
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

        if records_buffer:
            HPDBFileRecord.objects.bulk_create(records_buffer)

        logger.info(f"Parsed {len(self.states)} states and {len(self.counties)} counties")

    def parse_directory(self, directory: str, limit: Optional[int] = None) -> Dict[str, int]:
        """Parse an HPDB directory containing hpdb.cfg and s_*.hpd files."""
        self._hpdb_base_dir = directory
        hpdb_cfg = os.path.join(directory, 'hpdb.cfg')
        if not os.path.exists(hpdb_cfg):
            raise FileNotFoundError(f"hpdb.cfg not found: {hpdb_cfg}")

        if self.progress_callback:
            try:
                self.progress_callback({
                    'stage': 'config',
                    'current_file': os.path.basename(hpdb_cfg),
                    'processed_files': 0,
                    'total_files': 0
                })
            except Exception:
                pass

        self.parse_hpdb_cfg(hpdb_cfg)

        system_files = [
            os.path.join(directory, f)
            for f in os.listdir(directory)
            if f.startswith('s_') and f.endswith('.hpd')
        ]
        system_files.sort()

        if limit:
            system_files = system_files[:limit]

        total_files = len(system_files)
        if self.progress_callback:
            try:
                self.progress_callback({
                    'stage': 'systems',
                    'current_file': '',
                    'processed_files': 0,
                    'total_files': total_files
                })
            except Exception:
                pass

        for index, file_path in enumerate(system_files, start=1):
            if self.progress_callback:
                try:
                    self.progress_callback({
                        'stage': 'systems',
                        'current_file': os.path.basename(file_path),
                        'processed_files': index - 1,
                        'total_files': total_files
                    })
                except Exception:
                    pass
            self.parse_system_file(file_path)
            if self.progress_callback:
                try:
                    self.progress_callback({
                        'stage': 'systems',
                        'current_file': os.path.basename(file_path),
                        'processed_files': index,
                        'total_files': total_files
                    })
                except Exception:
                    pass

        return {
            'states': len(self.states),
            'counties': len(self.counties),
            'systems': len(system_files),
        }
    
    def _parse_state_info(self, parts: List[str]):
        """Parse StateInfo line from hpdb.cfg"""
        # Format: StateInfo\tStateId=X\tCountryId=Y\tName\tCode
        # Positions: [0]=Type, [1]=StateId=X, [2]=CountryId=Y, [3]=Name, [4]=Code
        if len(parts) < 5:
            return
        
        try:
            state_id = int(parts[1].split('=')[1])
            country_id = int(parts[2].split('=')[1])
            name = parts[3].strip()
            code = parts[4].strip()
            
            # Nationwide special case: CountryId=0 and StateId=0
            if state_id == 0 and country_id == 0:
                self._ensure_nationwide()
                return

            # Skip StateId=0 (used for _MultipleStates)
            if state_id == 0:
                return
            
            # Create or update country
            if country_id not in self.countries:
                country_name = 'USA' if country_id == 1 else 'Canada' if country_id == 2 else f'Country {country_id}'
                country, _ = Country.objects.using('hpdb').update_or_create(
                    country_id=country_id,
                    defaults={'name_tag': country_name, 'code': ''}
                )
                self.countries[country_id] = country
            
            # Create or update state
            state, created = State.objects.using('hpdb').update_or_create(
                state_id=state_id,
                defaults={
                    'country': self.countries[country_id],
                    'name_tag': name,
                    'short_name': code
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
        # Positions: [0]=Type, [1]=CountyId=X, [2]=StateId=Y, [3]=Name
        if len(parts) < 4:
            return
        
        try:
            county_id = int(parts[1].split('=')[1])
            state_id = int(parts[2].split('=')[1])
            name = parts[3].strip()

            # Statewide special case: CountyId=0
            if county_id == 0:
                return

            if state_id == 0:
                self._ensure_nationwide()
                state_id = 0
            
            if state_id not in self.states:
                logger.warning(f"State {state_id} not found for county {name}")
                return
            
            county, created = County.objects.using('hpdb').update_or_create(
                county_id=county_id,
                defaults={
                    'state': self.states[state_id],
                    'name_tag': name
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

        if not self._hpdb_base_dir:
            self._hpdb_base_dir = os.path.dirname(file_path)

        self._store_raw_file(file_path)

        # Reset handler stats for this file
        self.record_handler.stats.clear()
        self.record_handler.unrecognized_types.clear()

        current_agency = None
        current_group = None
        current_frequency = None
        self._current_agency = None
        self._current_group = None
        self._current_site_id = None

        records_buffer: List[HPDBFileRecord] = []

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_number, raw_line in enumerate(f, start=1):
                raw_line = raw_line.rstrip('\n').rstrip('\r')
                if not raw_line:
                    continue

                record = self._build_file_record(raw_line, line_number, file_path)
                records_buffer.append(record)
                if len(records_buffer) >= 2000:
                    HPDBFileRecord.objects.bulk_create(records_buffer)
                    records_buffer.clear()

                line = raw_line.strip()
                if not line:
                    continue

                # Use RecordHandler to parse the line
                self.record_handler.parse_line(line, line_number)

                # Handle context-dependent records (requires current_agency, current_group)
                parts = line.split('\t')
                if len(parts) < 2:
                    continue

                record_type = parts[0]

                # Track context for nested records
                if record_type == 'Conventional' or record_type == 'Trunk':
                    current_agency = self._parse_agency(parts, record_type, line_number, line)
                    current_group = None
                    current_frequency = None
                    self._current_agency = current_agency
                    self._current_group = None
                    self._current_site_id = None
                elif record_type == 'AreaState' and current_agency:
                    self._parse_area_state(parts, current_agency, line_number, line)
                elif record_type == 'AreaCounty' and current_agency:
                    self._parse_area_county(parts, current_agency, line_number, line)
                elif record_type == 'C-Group' and current_agency:
                    current_group = self._parse_channel_group(parts, current_agency, line_number, line)
                    current_frequency = None
                    self._current_group = current_group
                elif record_type == 'C-Freq' and current_group:
                    self._parse_frequency(parts, current_group, line_number, line)
                    current_frequency = None
                elif record_type == 'Site':
                    site_id = BaseRecordParser.extract_id(parts[1], 'SiteId') if len(parts) > 1 else None
                    self._current_site_id = site_id

        if records_buffer:
            HPDBFileRecord.objects.bulk_create(records_buffer)

        # Log summary
        self.record_handler.log_summary()
        logger.info(f"Completed parsing {file_path}")

    def _store_raw_file(self, file_path: str):
        """Store raw file content for reconstruction (development only)."""
        file_name = os.path.basename(file_path)
        file_type = file_name.split('.')[-1].lower() if '.' in file_name else ''

        # Remove previous raw entries for same file name to prevent duplication
        HPDBRawFile.objects.filter(file_name=file_name).delete()

        raw_file = HPDBRawFile.objects.create(
            file_name=file_name,
            file_type=file_type,
            file_size=os.path.getsize(file_path),
        )

        raw_lines = []
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for idx, raw_line in enumerate(f, start=1):
                raw_lines.append(HPDBRawLine(
                    raw_file=raw_file,
                    line_number=idx,
                    content=raw_line.rstrip('\n').rstrip('\r'),
                ))
        HPDBRawLine.objects.bulk_create(raw_lines)

    def _build_file_record(self, raw_line: str, line_number: int, file_path: str) -> HPDBFileRecord:
        """Build a structured file record that preserves field order and trailing empties."""
        trailing_empty = len(raw_line) - len(raw_line.rstrip('\t'))
        parts = raw_line.split('\t')
        record_type = parts[0] if parts else ''
        fields = parts[1:] if len(parts) > 1 else []
        spec_field_order, spec_field_map = build_spec_field_map(record_type, fields)

        rel_path = os.path.relpath(file_path, self._hpdb_base_dir) if self._hpdb_base_dir else os.path.basename(file_path)
        file_rel = os.path.join('HPDB', rel_path).replace('\\', '/')

        return HPDBFileRecord(
            file_name=os.path.basename(file_path),
            file_path=file_rel,
            record_type=record_type,
            fields=fields,
            spec_field_order=spec_field_order,
            spec_field_map=spec_field_map,
            trailing_empty_fields=trailing_empty,
            line_number=line_number,
        )
    
    def _parse_agency(self, parts: List[str], system_type: str, line_number: int = 0, raw_source: str = '') -> Optional[HPDBAgency]:
        """Parse Conventional or Trunk agency line"""
        # Format: Conventional\tAgencyId=X\tStateId=Y\tName\tOn/Off\tSystemType
        # Positions: [0]=Type, [1]=AgencyId=X, [2]=StateId=Y, [3]=Name, [4]=On/Off, [5]=SystemType
        raw_line = '\t'.join(parts)
        if len(parts) < 5:
            logger.warning(f"Line {line_number}: Agency record has insufficient fields (< 5): {raw_source[:100]}")
            return None
        
        try:
            agency_id = int(parts[1].split('=')[1])
            state_id = int(parts[2].split('=')[1])
            name = parts[3].strip()
            enabled = (parts[4].strip() == 'On')
            
            if not name:
                logger.warning(f"Line {line_number}: Agency has no name: {raw_source[:100]}")
                return None
            
            agency, created = HPDBAgency.objects.using('hpdb').update_or_create(
                agency_id=agency_id,
                defaults={
                    'name_tag': name,
                    'system_type': system_type,
                    'enabled': enabled,
                    'raw_data': raw_line
                }
            )

            if state_id == 0:
                self._ensure_nationwide()
            if state_id in self.states:
                agency.states.add(self.states[state_id])

            self.agencies[agency_id] = agency
            
            if created:
                logger.debug(f"Line {line_number}: Created agency: {name} ({system_type})")
            else:
                logger.debug(f"Line {line_number}: Updated agency: {name} ({system_type})")
            
            return agency
        
        except (IndexError, ValueError) as e:
            logger.warning(f"Line {line_number}: Error parsing agency - {e}: {raw_source[:100]}")
            return None
    
    def _parse_area_state(self, parts: List[str], agency: HPDBAgency, line_number: int = 0, raw_source: str = ''):
        """Parse AreaState line to link agency to states"""
        # Format: AreaState\tAgencyId=X\tStateId=Y
        # Positions: [0]=Type, [1]=AgencyId=X, [2]=StateId=Y
        if len(parts) < 3:
            logger.warning(f"Line {line_number}: AreaState record has insufficient fields (< 3): {raw_source[:100]}")
            return
        
        try:
            state_id = int(parts[2].split('=')[1])

            if state_id == 0:
                self._ensure_nationwide()
            
            if state_id in self.states and state_id != 0:
                agency.states.add(self.states[state_id])
            elif state_id == 0 and 0 in self.states:
                agency.states.add(self.states[0])
        
        except (IndexError, ValueError) as e:
            logger.warning(f"Line {line_number}: Error parsing AreaState - {e}: {raw_source[:100]}")
    
    def _parse_area_county(self, parts: List[str], agency: HPDBAgency, line_number: int = 0, raw_source: str = ''):
        """Parse AreaCounty line to link agency to counties"""
        # Format: AreaCounty\tAgencyId=X\tCountyId=Y
        # Positions: [0]=Type, [1]=AgencyId=X, [2]=CountyId=Y
        # Note: CountyId=0 means statewide/nationwide (not specific to a county)
        if len(parts) < 3:
            logger.warning(f"Line {line_number}: AreaCounty record has insufficient fields (< 3): {raw_source[:100]}")
            return
        
        try:
            county_id = int(parts[2].split('=')[1])
            
            # Only add to specific counties if CountyId is not 0
            # CountyId=0 means "statewide" or "nationwide" - these appear under the state node
            if county_id == 0:
                logger.debug(f"Line {line_number}: AreaCounty with CountyId=0 (statewide)")
                return
            if county_id in self.counties:
                agency.counties.add(self.counties[county_id])
            # If CountyId=0, the agency will appear under the state (via the states relationship)
        
        except (IndexError, ValueError) as e:
            logger.warning(f"Line {line_number}: Error parsing AreaCounty - {e}: {raw_source[:100]}")
    
    def _parse_channel_group(self, parts: List[str], agency: HPDBAgency, line_number: int = 0, raw_source: str = '') -> Optional[HPDBChannelGroup]:
        """Parse C-Group line"""
        # Format: C-Group\tCGroupId=X\tAgencyId=Y\tName\tOn/Off\tLatitude\tLongitude\tRange\tLocationType
        # Positions: [0]=Type, [1]=CGroupId=X, [2]=AgencyId=Y, [3]=Name, [4]=On/Off, [5]=Lat, [6]=Lon, [7]=Range, [8]=LocType
        raw_line = '\t'.join(parts)
        if len(parts) < 9:
            logger.warning(f"Line {line_number}: C-Group record has insufficient fields (< 9): {raw_source[:100]}")
            return None
        
        try:
            cgroup_id = int(parts[1].split('=')[1])
            name = parts[3].strip()
            enabled = (parts[4].strip() == 'On')
            
            # Extract coordinates and range from fixed positions
            latitude = None
            longitude = None
            range_miles = None
            
            if parts[5]:
                latitude = float(parts[5])
            if parts[6]:
                longitude = float(parts[6])
            if parts[7]:
                range_miles = float(parts[7])
            
            location_type = parts[8].strip() if len(parts) > 8 else ''
            
            if cgroup_id is None:
                return None
            
            group, created = HPDBChannelGroup.objects.using('hpdb').update_or_create(
                cgroup_id=cgroup_id,
                agency=agency,
                defaults={
                    'name_tag': name,
                    'enabled': enabled,
                    'latitude': latitude,
                    'longitude': longitude,
                    'range_miles': range_miles,
                    'location_type': location_type,
                    'raw_data': raw_line
                }
            )

            self.channel_groups[cgroup_id] = group
            
            # Apply any cached rectangles for this channel group
            # The rectangle cache uses the MyId value from parts[1] (e.g., "CGroupId=123")
            rectangle_key = parts[1].strip()  # This is the MyId from the C-Group record
            if rectangle_key in self._rectangles_cache:
                for rect_data in self._rectangles_cache[rectangle_key]:
                    HPDBRectangle.objects.using('hpdb').create(
                        channel_group=group,
                        latitude_1=rect_data['latitude_1'],
                        longitude_1=rect_data['longitude_1'],
                        latitude_2=rect_data['latitude_2'],
                        longitude_2=rect_data['longitude_2']
                    )
                logger.debug(f"Applied {len(self._rectangles_cache[rectangle_key])} rectangles to channel group {name}")
            
            if created:
                logger.debug(f"Created channel group: {name}")
            else:
                logger.debug(f"Updated channel group: {name}")
            
            return group
        
        except (IndexError, ValueError) as e:
            logger.warning(f"Error parsing channel group: {parts} - {e}")
            return None
    
    def _parse_frequency(self, parts: List[str], group: HPDBChannelGroup, line_number: int = 0, raw_source: str = ''):
        """Parse C-Freq line"""
        # Format: C-Freq\tCFreqId=X\tCGroupId=Y\tDescription\tOn/Off\tFrequency\tModulation\tTone/NAC\tDelay
        # Positions: [0]=Type, [1]=CFreqId=X, [2]=CGroupId=Y, [3]=Description, [4]=On/Off, [5]=Frequency, [6]=Modulation, [7]=Tone/NAC, [8]=Delay
        raw_line = '\t'.join(parts)
        try:
            cfreq_id = None
            description = ''
            enabled = False
            frequency = None
            modulation = ''
            tone = ''
            delay = 15
            
            # Extract CFreqId from key=value pair
            for part in parts:
                if part.startswith('CFreqId='):
                    cfreq_id = int(part.split('=')[1])
            
            # Parse based on fixed positions
            if len(parts) >= 6:
                # [3] = Description (may be empty)
                description = parts[3].strip() if parts[3] else ''
                
                # [4] = On/Off status
                enabled = (parts[4].strip() == 'On') if len(parts) > 4 else False
                
                # [5] = Frequency (MUST be numeric and in Hz range for radio frequencies)
                if len(parts) > 5 and parts[5].isdigit():
                    freq_value = int(parts[5])
                    # Validate it's a reasonable frequency in Hz (UHF/VHF range: 25 MHz to 10 GHz)
                    if 25000000 <= freq_value <= 10000000000:
                        frequency = freq_value
                
                # [6] = Modulation
                if len(parts) > 6 and parts[6].strip() in ['AM', 'FM', 'NFM', 'AUTO', 'DSB']:
                    modulation = parts[6].strip()
                
                # [7] = Tone/NAC (AudioOption per spec)
                if len(parts) > 7 and parts[7]:
                    tone_part = parts[7].strip()
                    if tone_part.startswith('TONE=') or tone_part.startswith('NAC='):
                        tone = tone_part
                
                # [8] = Delay (in seconds/milliseconds)
                if len(parts) > 8 and parts[8].isdigit():
                    try:
                        delay = int(parts[8])
                    except (ValueError, TypeError):
                        pass
            
            if cfreq_id is None or frequency is None:
                logger.warning(f"Line {line_number}: C-Freq missing cfreq_id or frequency: {raw_source[:100]}")
                return
            
            freq, created = HPDBFrequency.objects.using('hpdb').update_or_create(
                cfreq_id=cfreq_id,
                cgroup=group,
                defaults={
                    'name_tag': '',
                    'description': description,
                    'enabled': enabled,
                    'frequency': frequency,
                    'modulation': modulation,
                    'audio_option': tone,
                    'delay': delay,
                    'raw_data': raw_line
                }
            )
            
            if created:
                logger.debug(f"Created frequency: {description or 'unnamed'} - {frequency/1000000:.6f} MHz")
            else:
                logger.debug(f"Updated frequency: {description or 'unnamed'} - {frequency/1000000:.6f} MHz")

        except (IndexError, ValueError) as e:
            logger.warning(f"Error parsing frequency: {parts} - {e}")
            return

    def _resolve_agency(self, parts: List[str]) -> Optional[HPDBAgency]:
        for part in parts:
            if part.startswith('AgencyId='):
                try:
                    agency_id = int(part.split('=')[1])
                except (IndexError, ValueError):
                    return None
                if agency_id in self.agencies:
                    return self.agencies[agency_id]
                agency = HPDBAgency.objects.using('hpdb').filter(agency_id=agency_id).first()
                if agency:
                    self.agencies[agency_id] = agency
                return agency
        return None

    def _resolve_group(self, parts: List[str]) -> Optional[HPDBChannelGroup]:
        for part in parts:
            if part.startswith('CGroupId='):
                try:
                    cgroup_id = int(part.split('=')[1])
                except (IndexError, ValueError):
                    return None
                if cgroup_id in self.channel_groups:
                    return self.channel_groups[cgroup_id]
                group = HPDBChannelGroup.objects.using('hpdb').filter(cgroup_id=cgroup_id).first()
                if group:
                    self.channel_groups[cgroup_id] = group
                return group
        return None


    def _parse_rectangle(self, parts: List[str], line_number: int = 0, raw_source: str = ''):
        """Parse Rectangle geographic coverage record (North, West, South, East bounds)
        Format: Rectangle\tMyId\tLatitude1\tLongitude1\tLatitude2\tLongitude2
        Notes: Spec indicates this is additional info for Department (C-Group) or Site.
        """
        try:
            if len(parts) < 6:
                logger.warning(f"Line {line_number}: Rectangle record has insufficient fields (< 6): {raw_source[:100]}")
                return

            my_id = parts[1].strip()
            coords = [p.strip() for p in parts[2:6]]

            if len(coords) == 4 and all(coords):
                try:
                    latitude_1 = float(coords[0])
                    longitude_1 = float(coords[1])
                    latitude_2 = float(coords[2])
                    longitude_2 = float(coords[3])
                    
                    rectangle_payload = {
                        'latitude_1': latitude_1,
                        'longitude_1': longitude_1,
                        'latitude_2': latitude_2,
                        'longitude_2': longitude_2,
                    }

                    # If the referenced channel group already exists, attach immediately.
                    # Otherwise, cache for later association when the group is parsed.
                    attached = False
                    if my_id.startswith('CGroupId='):
                        try:
                            cgroup_id = int(my_id.split('=')[1])
                        except (IndexError, ValueError):
                            cgroup_id = None

                        if cgroup_id is not None:
                            group = self.channel_groups.get(cgroup_id)
                            if group is None:
                                group = HPDBChannelGroup.objects.using('hpdb').filter(cgroup_id=cgroup_id).first()
                                if group:
                                    self.channel_groups[cgroup_id] = group

                            if group:
                                HPDBRectangle.objects.using('hpdb').create(
                                    channel_group=group,
                                    **rectangle_payload
                                )
                                attached = True

                    if not attached:
                        if my_id not in self._rectangles_cache:
                            self._rectangles_cache[my_id] = []
                        self._rectangles_cache[my_id].append(rectangle_payload)
                    
                    association = None
                    if self._current_group is not None:
                        association = 'Department'
                    elif self._current_site_id is not None:
                        association = 'Site'

                    logger.debug(
                        f"Line {line_number}: Parsed Rectangle geographic coverage: "
                        f"Id={my_id}, Lat1={latitude_1}, Lon1={longitude_1}, "
                        f"Lat2={latitude_2}, Lon2={longitude_2}, Assoc={association}"
                    )
                except (ValueError, IndexError) as e:
                    logger.warning(f"Line {line_number}: Rectangle has invalid coordinate values - {e}: {raw_source[:100]}")
            else:
                logger.warning(f"Line {line_number}: Rectangle record has insufficient coordinates (< 4): {raw_source[:100]}")
        except Exception as e:
            logger.warning(f"Line {line_number}: Error parsing Rectangle - {e}: {raw_source[:100]}")

    def _parse_circle(self, parts: List[str], line_number: int = 0, raw_source: str = ''):
        """Parse Circle geographic coverage record
        These are standalone coverage areas, not tied to specific C-Groups.
        Format: Circle\tMyId\tLatitude\tLongitude\tRadius
        """
        try:
            if len(parts) < 5:
                logger.debug(f"Line {line_number}: Parsed Circle geographic coverage record (no coords)")
                return

            my_id = parts[1].strip()
            coords = [p.strip() for p in parts[2:5]]
            if len(coords) == 3 and all(coords):
                try:
                    latitude = float(coords[0])
                    longitude = float(coords[1])
                    radius = float(coords[2])
                    logger.debug(f"Line {line_number}: Parsed Circle geographic coverage: "
                               f"Id={my_id}, Lat={latitude}, Lon={longitude}, Radius={radius}")
                except (ValueError, IndexError) as e:
                    logger.warning(f"Line {line_number}: Circle has invalid coordinate values - {e}: {raw_source[:100]}")
            else:
                logger.debug(f"Line {line_number}: Parsed Circle geographic coverage record (minimal)")
        except Exception as e:
            logger.warning(f"Line {line_number}: Error parsing Circle - {e}: {raw_source[:100]}")

    def _parse_lm_site(self, parts: List[str], line_number: int = 0, raw_source: str = ''):
        """Parse LM (trunk link/site) record
        Format: LM\tStateId=X\tCountyId=Y\tTrunkId=Z\tSiteId=W\t[enabled]\t[reserved]\tLatitude\tLongitude
        """
        try:
            state_id = None
            county_id = None
            trunk_id = None
            site_id = None
            latitude = None
            longitude = None
            
            for part in parts[1:]:
                if part.startswith('StateId='):
                    try:
                        state_id = int(part.split('=')[1])
                    except ValueError:
                        logger.warning(f"Line {line_number}: LM has invalid StateId format: {raw_source[:100]}")
                elif part.startswith('CountyId='):
                    try:
                        county_id = int(part.split('=')[1])
                    except ValueError:
                        logger.warning(f"Line {line_number}: LM has invalid CountyId format: {raw_source[:100]}")
                elif part.startswith('TrunkId='):
                    try:
                        trunk_id = int(part.split('=')[1])
                    except ValueError:
                        logger.warning(f"Line {line_number}: LM has invalid TrunkId format: {raw_source[:100]}")
                elif part.startswith('SiteId='):
                    try:
                        site_id = int(part.split('=')[1])
                    except ValueError:
                        logger.warning(f"Line {line_number}: LM has invalid SiteId format: {raw_source[:100]}")
            
            # Extract latitude and longitude from end of line
            if len(parts) >= 9:
                try:
                    latitude = float(parts[-2])
                    longitude = float(parts[-1])
                except (IndexError, ValueError):
                    logger.warning(f"Line {line_number}: LM has invalid lat/long: {raw_source[:100]}")
            
            logger.debug(f"Line {line_number}: Parsed LM site: StateId={state_id}, CountyId={county_id}, "
                        f"TrunkId={trunk_id}, SiteId={site_id}, Lat={latitude}, Lng={longitude}")
        except Exception as e:
            logger.warning(f"Line {line_number}: Error parsing LM site - {e}: {raw_source[:100]}")

    def _parse_lm_frequency(self, parts: List[str], line_number: int = 0, raw_source: str = ''):
        """Parse LM_FREQUENCY (trunk frequency) record"""
        try:
            # Format typically: LM_FREQUENCY\t[frequency data]
            logger.debug(f"Line {line_number}: Parsed LM_FREQUENCY: {raw_source[:100]}")
        except Exception as e:
            logger.warning(f"Line {line_number}: Error parsing LM_FREQUENCY - {e}: {raw_source[:100]}")
    
    # Handler wrapper methods for RecordHandler integration
    def _handle_target_model(self, parts: List[str], line_number: int, raw_source: str):
        """Handle TargetModel record (file metadata)"""
        logger.debug(f"Line {line_number}: TargetModel: {raw_source}")
    
    def _handle_format_version(self, parts: List[str], line_number: int, raw_source: str):
        """Handle FormatVersion record (file metadata)"""
        logger.debug(f"Line {line_number}: FormatVersion: {raw_source}")
    
    def _handle_date_modified(self, parts: List[str], line_number: int, raw_source: str):
        """Handle DateModified record (file metadata)"""
        logger.debug(f"Line {line_number}: DateModified: {raw_source}")
    
    def _handle_state_info(self, parts: List[str], line_number: int, raw_source: str):
        """Handle StateInfo record (configuration)"""
        self._parse_state_info(parts)
    
    def _handle_county_info(self, parts: List[str], line_number: int, raw_source: str):
        """Handle CountyInfo record (configuration)"""
        self._parse_county_info(parts)
    
    def _handle_conventional(self, parts: List[str], line_number: int, raw_source: str):
        """Handle Conventional agency record"""
        self._parse_agency(parts, 'Conventional', line_number, raw_source)
    
    def _handle_trunk(self, parts: List[str], line_number: int, raw_source: str):
        """Handle Trunk system record"""
        self._parse_agency(parts, 'Trunk', line_number, raw_source)
    
    def _handle_area_state(self, parts: List[str], line_number: int, raw_source: str):
        """Handle AreaState record"""
        # Delegate to existing method - requires current_agency context
        # This will be handled differently in refactored version
        logger.debug(f"Line {line_number}: AreaState record")
    
    def _handle_area_county(self, parts: List[str], line_number: int, raw_source: str):
        """Handle AreaCounty record"""
        # Delegate to existing method - requires current_agency context
        logger.debug(f"Line {line_number}: AreaCounty record")
    
    def _handle_c_group(self, parts: List[str], line_number: int, raw_source: str):
        """Handle C-Group (channel group) record"""
        logger.debug(f"Line {line_number}: C-Group record")
    
    def _handle_c_freq(self, parts: List[str], line_number: int, raw_source: str):
        """Handle C-Freq (conventional frequency) record"""
        logger.debug(f"Line {line_number}: C-Freq record")
    
    def _handle_rectangle(self, parts: List[str], line_number: int, raw_source: str):
        """Handle Rectangle geographic coverage record"""
        self._parse_rectangle(parts, line_number, raw_source)
    
    def _handle_circle(self, parts: List[str], line_number: int, raw_source: str):
        """Handle Circle geographic coverage record"""
        self._parse_circle(parts, line_number, raw_source)
    
    def _handle_site(self, parts: List[str], line_number: int, raw_source: str):
        """Handle Site (trunk system site) record"""
        logger.debug(f"Line {line_number}: Site record (trunk system)")
    
    def _handle_t_group(self, parts: List[str], line_number: int, raw_source: str):
        """Handle T-Group (trunk group) record"""
        logger.debug(f"Line {line_number}: T-Group record")
    
    def _handle_t_freq(self, parts: List[str], line_number: int, raw_source: str):
        """Handle T-Freq (trunk frequency) record"""
        logger.debug(f"Line {line_number}: T-Freq record")
    
    def _handle_tgid(self, parts: List[str], line_number: int, raw_source: str):
        """Handle TGID (Talk Group ID) record"""
        logger.debug(f"Line {line_number}: TGID record")
    
    def _handle_lm_site(self, parts: List[str], line_number: int, raw_source: str):
        """Handle LM (trunk link/site) record"""
        self._parse_lm_site(parts, line_number, raw_source)
    
    def _handle_lm_frequency(self, parts: List[str], line_number: int, raw_source: str):
        """Handle LM_FREQUENCY (trunk frequency) record"""
        self._parse_lm_frequency(parts, line_number, raw_source)
    
    def _handle_fleet_map(self, parts: List[str], line_number: int, raw_source: str):
        """Handle FleetMap record"""
        logger.debug(f"Line {line_number}: FleetMap record")
    
    def _handle_unit_ids(self, parts: List[str], line_number: int, raw_source: str):
        """Handle UnitIds record"""
        logger.debug(f"Line {line_number}: UnitIds record")
    
    def _handle_avoid_tgids(self, parts: List[str], line_number: int, raw_source: str):
        """Handle AvoidTgids record"""
        logger.debug(f"Line {line_number}: AvoidTgids record")
    
    def _handle_band_plan_mot(self, parts: List[str], line_number: int, raw_source: str):
        """Handle BandPlan_Mot record"""
        logger.debug(f"Line {line_number}: BandPlan_Mot record")
    
    def _handle_band_plan_p25(self, parts: List[str], line_number: int, raw_source: str):
        """Handle BandPlan_P25 record"""
        logger.debug(f"Line {line_number}: BandPlan_P25 record")
    
    def _handle_dqks_status(self, parts: List[str], line_number: int, raw_source: str):
        """Handle DQKs_Status record"""
        logger.debug(f"Line {line_number}: DQKs_Status record")


class FavoritesListParser:
    """Parser for f_list.cfg file"""
    
    @staticmethod
    def parse_favorites_list(file_path: str):
        """Parse f_list.cfg file"""
        from .models import FavoritesList
        import json
        
        logger.info(f"Parsing favorites list: {file_path}")
        
        FavoritesList.objects.all().delete()  # Clear existing
        
        order = 0
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
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
        
        logger.info(f"Parsed {order} favorites lists")
