"""Parser for Favorites List files from favorites_lists folder"""
import os
import logging
from .models import ScannerFileRecord
from .record_parser.spec_field_maps import build_spec_field_map

logger = logging.getLogger(__name__)


class FavoritesListParser:
    """Parser for f_list.cfg file"""
    
    @staticmethod
    def parse_favorites_list(file_path: str):
        """Parse f_list.cfg file"""
        from .models import FavoritesList
        import json
        
        logger.info(f"Parsing favorites list: {file_path}")
        
        FavoritesList.objects.all().delete()  # Clear existing

        target_model = 'BCDx36HP'
        format_version = '1.00'

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
                    spec_field_order, spec_field_map = build_spec_field_map(record_type, fields)

                    records_buffer.append(ScannerFileRecord(
                        file_name=os.path.basename(file_path),
                        file_path='favorites_lists/f_list.cfg',
                        record_type=record_type,
                        fields=fields,
                        spec_field_order=spec_field_order,
                        spec_field_map=spec_field_map,
                        trailing_empty_fields=trailing_empty,
                        line_number=line_number,
                    ))

                    if len(records_buffer) >= 2000:
                        ScannerFileRecord.objects.bulk_create(records_buffer)
                        records_buffer.clear()

                line = raw_line.strip()
                if not line:
                    continue

                parts = parts_all

                if line.startswith('TargetModel'):
                    target_model = parts[1].strip() if len(parts) > 1 else target_model
                    continue

                if line.startswith('FormatVersion'):
                    format_version = parts[1].strip() if len(parts) > 1 else format_version
                    continue
                
                parts = line.split('\t')
                if len(parts) < 7:
                    continue
                
                # Check for F-List record (may have trailing space in first column)
                if not parts[0].strip().startswith('F-List'):
                    continue
                
                try:
                    user_name = parts[1].strip() if len(parts) > 1 else ''
                    filename = parts[2].strip() if len(parts) > 2 else ''
                    location_control = parts[3].strip() if len(parts) > 3 else 'Off'
                    monitor = parts[4].strip() if len(parts) > 4 else 'Off'
                    quick_key = parts[5].strip() if len(parts) > 5 else 'Off'
                    number_tag = parts[6].strip() if len(parts) > 6 else 'Off'
                    
                    # StartupKey0-9 (10 fields at parts[7:17])
                    startup_keys = [parts[i].strip() if len(parts) > i else 'Off' for i in range(7, 17)]
                    
                    # S-Qkey_00 to S-Qkey_99 (100 fields at parts[17:117])
                    s_qkeys = [parts[i].strip() if len(parts) > i else 'Off' for i in range(17, 117)]
                    
                    FavoritesList.objects.using('favorites').create(
                        user_name=user_name,
                        filename=filename,
                        scanner_model=target_model,
                        format_version=format_version,
                        location_control=location_control,
                        monitor=monitor,
                        quick_key=quick_key,
                        number_tag=number_tag,
                        order=order,
                        startup_keys=startup_keys,
                        s_qkeys=s_qkeys,
                        raw_data=line
                    )
                    
                    order += 1
                    logger.debug(f"Created favorites list: {user_name} ({filename})")
                
                except (IndexError, ValueError) as e:
                    logger.warning(f"Error parsing favorites list: {parts} - {e}")
        
        if records_buffer:
            ScannerFileRecord.objects.bulk_create(records_buffer)

        logger.info(f"Parsed {order} favorites lists")
