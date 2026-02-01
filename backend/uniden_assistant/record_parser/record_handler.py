"""Core record type parser handling all HomePatrol data file formats"""
import logging
from typing import Dict, List, Optional, Callable, Any

logger = logging.getLogger(__name__)


class RecordHandler:
    """
    Shared record type parser for HomePatrol files (HPDB, Favorites, scanner.inf, profile.cfg, etc).
    
    Handles parsing of all record types defined in HomePatrol specification.
    Routes each record type to appropriate handler callbacks.
    
    Usage:
        handler = RecordHandler(using_db='hpdb')
        handler.register_handler('Conventional', callback_fn)
        handler.parse_line(line_content, line_number=123)
    """
    
    # All record types from HomePatrol specification
    KNOWN_RECORD_TYPES = {
        # File metadata
        'TargetModel', 'FormatVersion', 'DateModified',
        
        # Configuration records
        'StateInfo', 'CountyInfo',
        
        # Conventional system records
        'Conventional', 'AreaState', 'AreaCounty', 'C-Group', 'C-Freq',
        
        # Conventional frequency details
        'Rectangle', 'Circle',
        
        # Trunk system records
        'Trunk', 'Site', 'T-Group', 'T-Freq', 'TGID', 'LM', 'LM_FREQUENCY',
        'FleetMap', 'UnitIds', 'AvoidTgids',
        
        # Band plan and advanced features
        'BandPlan_Mot', 'BandPlan_P25', 'DQKs_Status',
        
        # Favorites-specific
        'F-List',  # Favorites list definition (from spec review of f_list.cfg)
    }
    
    def __init__(self, using_db: str = 'default'):
        """
        Initialize the record handler.
        
        Args:
            using_db: Database alias to use (e.g., 'hpdb', 'usersettings', 'default')
        """
        self.using_db = using_db
        self.handlers: Dict[str, Callable] = {}
        self.unrecognized_types: Dict[str, List[tuple]] = {}  # type -> [(line_num, content)]
        self.stats: Dict[str, int] = {}  # Record type -> count
    
    def register_handler(self, record_type: str, callback: Callable[[List[str], int, str], None]):
        """
        Register a handler callback for a record type.
        
        Args:
            record_type: Record type name (e.g., 'Conventional', 'C-Freq')
            callback: Function(parts, line_number, raw_source) to handle this record type
        """
        self.handlers[record_type] = callback
    
    def parse_line(self, line: str, line_number: int = 0) -> bool:
        """
        Parse a single line from a HomePatrol file.
        
        Args:
            line: Raw line content
            line_number: Line number in source file (for error reporting)
            
        Returns:
            True if line was recognized and handled, False if unrecognized
        """
        line = line.strip()
        if not line:
            return True  # Empty lines are OK
        
        parts = line.split('\t')
        if len(parts) < 1:
            return False
        
        record_type = parts[0].strip()
        raw_source = line[:150]
        
        # Track statistics
        self.stats[record_type] = self.stats.get(record_type, 0) + 1
        
        # Check if we have a handler for this type
        if record_type in self.handlers:
            try:
                self.handlers[record_type](parts, line_number, raw_source)
                return True
            except Exception as e:
                logger.warning(f"Line {line_number}: Error in {record_type} handler - {e}: {raw_source}")
                return False
        
        # Check if it's a known type without a handler yet
        if record_type in self.KNOWN_RECORD_TYPES:
            logger.debug(f"Line {line_number}: Known record type '{record_type}' parsed but no handler registered: {raw_source}")
            return True
        
        # Unrecognized type
        if record_type not in self.unrecognized_types:
            self.unrecognized_types[record_type] = []
        self.unrecognized_types[record_type].append((line_number, raw_source))
        
        return False
    
    def get_stats(self) -> Dict[str, int]:
        """Get parsing statistics (record type -> count)"""
        return self.stats.copy()
    
    def get_unrecognized(self) -> Dict[str, List[tuple]]:
        """Get unrecognized record types and their locations"""
        return self.unrecognized_types.copy()
    
    def log_summary(self):
        """Log a summary of parsing results"""
        if self.stats:
            logger.info(f"Parsed records by type: {self.stats}")
        
        if self.unrecognized_types:
            logger.warning(f"Found {len(self.unrecognized_types)} unrecognized record types:")
            for record_type, instances in self.unrecognized_types.items():
                logger.warning(f"  '{record_type}': {len(instances)} instances "
                              f"(first: line {instances[0][0]}: {instances[0][1]})")
        
        # Check for known types that were found
        found_known = set(self.stats.keys()) & self.KNOWN_RECORD_TYPES
        if found_known:
            logger.info(f"Found {len(found_known)} known record types: {sorted(found_known)}")


class BaseRecordParser:
    """
    Base class for parsers that use RecordHandler.
    
    Provides utility methods for common parsing tasks:
    - ID extraction (StateId=X -> X)
    - Frequency validation
    - Coordinate parsing
    - Boolean parsing
    """
    
    @staticmethod
    def extract_id(part: str, id_name: str) -> Optional[int]:
        """
        Extract numeric ID from key=value format.
        
        Args:
            part: String like "StateId=42"
            id_name: Expected key name (e.g., "StateId")
            
        Returns:
            Numeric ID or None if not found/invalid
        """
        if not part.startswith(f'{id_name}='):
            return None
        try:
            return int(part.split('=', 1)[1])
        except (IndexError, ValueError):
            return None
    
    @staticmethod
    def extract_ids_from_parts(parts: List[str]) -> Dict[str, int]:
        """
        Extract all ID values from parts.
        
        Returns dict of id_name -> value for all parts matching *Id=* pattern.
        """
        ids = {}
        id_names = ['CountryId', 'StateId', 'CountyId', 'AgencyId', 'TrunkId', 
                    'SiteId', 'CGroupId', 'CFreqId', 'TGroupId', 'TFreqId', 'Tid']
        
        for part in parts:
            for id_name in id_names:
                value = BaseRecordParser.extract_id(part, id_name)
                if value is not None:
                    ids[id_name] = value
                    break
        
        return ids
    
    @staticmethod
    def parse_enabled(value: str) -> bool:
        """Parse On/Off or Yes/No to boolean"""
        return value.strip().lower() in ('on', 'yes', 'true', '1')
    
    @staticmethod
    def validate_frequency(frequency_hz: int) -> bool:
        """
        Validate frequency in Hz.
        
        Checks if frequency is in reasonable range for radio frequencies.
        Valid range: 25 MHz to 10 GHz (25,000,000 to 10,000,000,000 Hz)
        """
        return 25000000 <= frequency_hz <= 10000000000
    
    @staticmethod
    def validate_coordinates(latitude: float, longitude: float) -> bool:
        """Validate latitude/longitude coordinates"""
        return (-90 <= latitude <= 90) and (-180 <= longitude <= 180)
    
    @staticmethod
    def parse_coordinates(lat_str: str, lon_str: str) -> Optional[tuple]:
        """
        Parse latitude/longitude strings to floats.
        
        Returns:
            (latitude, longitude) tuple or None if invalid
        """
        try:
            lat = float(lat_str)
            lon = float(lon_str)
            if BaseRecordParser.validate_coordinates(lat, lon):
                return (lat, lon)
            return None
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def get_database_alias(context: Dict[str, Any]) -> str:
        """
        Get the database alias from parser context.
        
        Args:
            context: Parser context dict (typically from RecordHandler or parser instance)
            
        Returns:
            Database alias (default: 'default')
        """
        return context.get('using_db', 'default')
