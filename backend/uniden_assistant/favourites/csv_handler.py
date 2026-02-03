"""
CSV export/import handler for Favourite Lists
Supports importing and exporting complete Favourite Lists with Systems, Departments, and Channels
"""
import csv
import io
from typing import Dict, List, Tuple, Any
from .models import (
    FavoritesList, ConventionalSystem, TrunkSystem, CGroup, Frequency
)


class FavoritesListCSVHandler:
    """Handle CSV export and import for Favourite Lists"""

    # CSV Section markers
    SECTION_METADATA = 'METADATA'
    SECTION_CONVENTIONAL = 'CONVENTIONAL_SYSTEM'
    SECTION_TRUNK = 'TRUNK_SYSTEM'
    SECTION_DEPARTMENT = 'DEPARTMENT'
    SECTION_CHANNEL = 'CHANNEL'

    @staticmethod
    def export_to_csv(favorites_list: FavoritesList) -> str:
        """
        Export a Favourite List to CSV format
        
        Format:
        METADATA,name,user_name,scanner_model,format_version
        CONVENTIONAL_SYSTEM,order,name_tag,avoid,modulation,...
        CHANNEL,name_tag,frequency,modulation,...
        TRUNK_SYSTEM,order,name_tag,system_type,...
        DEPARTMENT,name_tag,...
        CHANNEL,name_tag,frequency,...
        """
        output = io.StringIO()
        writer = csv.writer(output)

        # Write metadata
        writer.writerow([
            'METADATA',
            favorites_list.user_name or '',
            favorites_list.scanner_model or 'BCDx36HP',
            favorites_list.format_version or '1.00',
        ])

        # Write Conventional Systems and their channels
        conventional = ConventionalSystem.objects.using('favorites').filter(
            favorites_list=favorites_list
        ).order_by('order')

        for conv_system in conventional:
            writer.writerow([
                'CONVENTIONAL_SYSTEM',
                conv_system.order,
                conv_system.name_tag or '',
                conv_system.avoid or 'Off',
                conv_system.system_type or '',
                conv_system.quick_key or 'Off',
            ])

            # Write channels for this conventional system
            channels = Frequency.objects.using('favorites').filter(
                cgroup__conventional_system=conv_system
            ).order_by('cgroup__order', 'order')

            for channel in channels:
                writer.writerow([
                    'CHANNEL',
                    channel.cgroup.name_tag or '',  # Department name
                    channel.name_tag or '',
                    channel.frequency or '',
                    channel.modulation or '',
                    channel.att_delay or '',
                    channel.offset or '',
                    channel.offset_direction or '',
                    channel.tone_mode or '',
                    channel.tone_freq or '',
                    channel.ctcss_decode or '',
                    channel.ctcss_encode or '',
                    channel.dcs_decode or '',
                    channel.dcs_encode or '',
                    channel.quick_key or 'Off',
                    channel.avoid or 'Off',
                ])

        # Write Trunk Systems and their sites/departments/channels
        trunked = TrunkSystem.objects.using('favorites').filter(
            favorites_list=favorites_list
        ).order_by('order')

        for trunk_system in trunked:
            writer.writerow([
                'TRUNK_SYSTEM',
                trunk_system.order,
                trunk_system.name_tag or '',
                trunk_system.system_type or 'P25Standard',
                trunk_system.avoid or 'Off',
                trunk_system.reserve or '',
                trunk_system.system_id_search or 'Srch',
            ])

            # Write departments for this trunk system
            departments = CGroup.objects.using('favorites').filter(
                trunk_system=trunk_system
            ).order_by('order')

            for dept in departments:
                writer.writerow([
                    'DEPARTMENT',
                    dept.name_tag or '',
                    dept.avoid or 'Off',
                    dept.quick_key or 'Off',
                ])

                # Write channels for this department
                channels = Frequency.objects.using('favorites').filter(
                    cgroup=dept
                ).order_by('order')

                for channel in channels:
                    writer.writerow([
                        'CHANNEL',
                        channel.name_tag or '',
                        channel.frequency or '',
                        channel.modulation or '',
                        channel.att_delay or '',
                        channel.offset or '',
                        channel.offset_direction or '',
                        channel.tone_mode or '',
                        channel.tone_freq or '',
                        channel.ctcss_decode or '',
                        channel.ctcss_encode or '',
                        channel.dcs_decode or '',
                        channel.dcs_encode or '',
                        channel.quick_key or 'Off',
                        channel.avoid or 'Off',
                    ])

        return output.getvalue()

    @staticmethod
    def import_from_csv(csv_content: str, favorites_list: FavoritesList) -> Tuple[int, List[str]]:
        """
        Import a Favourite List from CSV content
        Returns: (count of imported items, list of errors)
        """
        errors = []
        imported_count = 0
        
        try:
            reader = csv.reader(io.StringIO(csv_content))
            current_system = None
            current_department = None
            
            for row_num, row in enumerate(reader, 1):
                if not row or not row[0]:
                    continue

                section = row[0]

                try:
                    if section == FavoritesListCSVHandler.SECTION_METADATA:
                        # Update metadata
                        if len(row) > 1:
                            favorites_list.user_name = row[1]
                        if len(row) > 2:
                            favorites_list.scanner_model = row[2]
                        if len(row) > 3:
                            favorites_list.format_version = row[3]
                        favorites_list.save(using='favorites')
                        imported_count += 1

                    elif section == FavoritesListCSVHandler.SECTION_CONVENTIONAL:
                        # Create/update conventional system
                        current_system = ConventionalSystem.objects.using('favorites').update_or_create(
                            favorites_list=favorites_list,
                            order=int(row[1]) if len(row) > 1 and row[1] else 0,
                            defaults={
                                'name_tag': row[2] if len(row) > 2 else '',
                                'avoid': row[3] if len(row) > 3 else 'Off',
                                'modulation': row[4] if len(row) > 4 else 'AUTO',
                                'att_delay': row[5] if len(row) > 5 else '',
                            }
                        )[0]
                        current_department = None
                        imported_count += 1

                    elif section == FavoritesListCSVHandler.SECTION_TRUNK:
                        # Create/update trunk system
                        current_system = TrunkSystem.objects.using('favorites').update_or_create(
                            favorites_list=favorites_list,
                            order=int(row[1]) if len(row) > 1 and row[1] else 0,
                            defaults={
                                'name_tag': row[2] if len(row) > 2 else '',
                                'system_type': row[3] if len(row) > 3 else 'P25Standard',
                                'avoid': row[4] if len(row) > 4 else 'Off',
                                'reserve': row[5] if len(row) > 5 else '',
                                'system_id_search': row[6] if len(row) > 6 else 'Srch',
                            }
                        )[0]
                        current_department = None
                        imported_count += 1

                    elif section == FavoritesListCSVHandler.SECTION_DEPARTMENT:
                        # Create/update department (CGroup)
                        if isinstance(current_system, TrunkSystem):
                            current_department = CGroup.objects.using('favorites').create(
                                trunk_system=current_system,
                                name_tag=row[1] if len(row) > 1 else '',
                                avoid=row[2] if len(row) > 2 else 'Off',
                                quick_key=row[3] if len(row) > 3 else 'Off',
                                order=0,  # Will be set by save_to_db logic
                            )
                            imported_count += 1

                    elif section == FavoritesListCSVHandler.SECTION_CHANNEL:
                        # Create/update channel (Frequency)
                        if current_system:
                            if isinstance(current_system, ConventionalSystem):
                                # For conventional, department is the channel group (system-level group)
                                dept, _ = CGroup.objects.using('favorites').get_or_create(
                                    conventional_system=current_system,
                                    name_tag=row[1] if len(row) > 1 else 'Default',
                                    defaults={'order': 0}
                                )
                            else:
                                # For trunk, use the current department
                                dept = current_department

                            if dept:
                                Frequency.objects.using('favorites').create(
                                    cgroup=dept,
                                    name_tag=row[2] if len(row) > 2 else '',
                                    frequency=row[3] if len(row) > 3 else '',
                                    modulation=row[4] if len(row) > 4 else '',
                                    att_delay=row[5] if len(row) > 5 else '',
                                    offset=row[6] if len(row) > 6 else '',
                                    offset_direction=row[7] if len(row) > 7 else '',
                                    tone_mode=row[8] if len(row) > 8 else '',
                                    tone_freq=row[9] if len(row) > 9 else '',
                                    ctcss_decode=row[10] if len(row) > 10 else '',
                                    ctcss_encode=row[11] if len(row) > 11 else '',
                                    dcs_decode=row[12] if len(row) > 12 else '',
                                    dcs_encode=row[13] if len(row) > 13 else '',
                                    quick_key=row[14] if len(row) > 14 else 'Off',
                                    avoid=row[15] if len(row) > 15 else 'Off',
                                    order=0,
                                )
                                imported_count += 1

                except (ValueError, IndexError) as e:
                    errors.append(f"Row {row_num}: {str(e)}")

            return imported_count, errors

        except Exception as e:
            errors.append(f"CSV parsing error: {str(e)}")
            return 0, errors
