"""
JSON export/import handler for Favourite Lists
Supports exporting and importing complete Favourite Lists with Systems, Departments, and Channels
Allows multiple lists to be exported/imported together
"""
import json
import re
from typing import List, Dict, Any, Tuple
from .models import (
    FavoritesList, ConventionalSystem, TrunkSystem, CGroup, CFreq, TGroup, TGID
)


class FavoritesListJSONHandler:
    """Handle JSON export and import for Favourite Lists"""

    @staticmethod
    def export_to_json(favorites_lists: List[FavoritesList]) -> str:
        """
        Export one or more Favourite Lists to JSON format
        Returns a JSON string with complete data structure
        """
        data = {
            'version': '1.0',
            'format': 'uniden_favorites',
            'favorites_lists': []
        }

        for fav_list in favorites_lists:
            fav_data = {
                'id': str(fav_list.id),
                'user_name': fav_list.user_name,
                'filename': '',
                'scanner_model': fav_list.scanner_model,
                'format_version': fav_list.format_version,
                'location_control': fav_list.location_control,
                'monitor': fav_list.monitor,
                'quick_key': fav_list.quick_key,
                'number_tag': fav_list.number_tag,
                'conventional_systems': [],
                'trunk_systems': []
            }

            # Export Conventional Systems
            conventional = ConventionalSystem.objects.using('favorites').filter(
                favorites_list=fav_list
            ).order_by('order')

            for conv_system in conventional:
                conv_data = {
                    'order': conv_system.order,
                    'name_tag': conv_system.name_tag,
                    'avoid': conv_system.avoid,
                    'system_type': conv_system.system_type,
                    'quick_key': conv_system.quick_key,
                    'number_tag': conv_system.number_tag,
                    'system_hold_time': conv_system.system_hold_time,
                    'analog_agc': conv_system.analog_agc,
                    'digital_agc': conv_system.digital_agc,
                    'digital_waiting_time': conv_system.digital_waiting_time,
                    'digital_threshold_mode': conv_system.digital_threshold_mode,
                    'digital_threshold_level': conv_system.digital_threshold_level,
                    'dqks_status': conv_system.dqks_status,
                    'groups': []
                }

                # Export groups (channels) for this conventional system
                groups = CGroup.objects.using('favorites').filter(
                    conventional_system=conv_system
                ).order_by('order')

                for group in groups:
                    group_data = {
                        'order': group.order,
                        'name_tag': group.name_tag,
                        'avoid': group.avoid,
                        'latitude': str(group.latitude) if group.latitude else None,
                        'longitude': str(group.longitude) if group.longitude else None,
                        'range_miles': str(group.range_miles) if group.range_miles else None,
                        'location_type': group.location_type,
                        'quick_key': group.quick_key,
                        'filter': group.filter,
                        'channels': []
                    }

                    # Export channels
                    channels = CFreq.objects.using('favorites').filter(
                        cgroup=group
                    ).order_by('order')

                    for channel in channels:
                        channel_data = {
                            'order': channel.order,
                            'name_tag': channel.name_tag,
                            'avoid': channel.avoid,
                            'frequency': channel.frequency,
                            'modulation': channel.modulation,
                            'audio_option': channel.audio_option,
                            'func_tag_id': channel.func_tag_id,
                            'attenuator': channel.attenuator,
                            'delay': channel.delay,
                            'volume_offset': channel.volume_offset,
                            'alert_tone': channel.alert_tone,
                            'alert_volume': channel.alert_volume,
                            'alert_color': channel.alert_color,
                            'alert_pattern': channel.alert_pattern,
                            'number_tag': channel.number_tag,
                            'priority_channel': channel.priority_channel,
                        }
                        group_data['channels'].append(channel_data)

                    conv_data['groups'].append(group_data)

                fav_data['conventional_systems'].append(conv_data)

            # Export Trunk Systems
            trunked = TrunkSystem.objects.using('favorites').filter(
                favorites_list=fav_list
            ).order_by('order')

            for trunk_system in trunked:
                trunk_data = {
                    'order': trunk_system.order,
                    'name_tag': trunk_system.name_tag,
                    'system_type': trunk_system.system_type,
                    'avoid': trunk_system.avoid,
                    'reserve': trunk_system.reserve,
                    'system_id_search': trunk_system.system_id_search,
                    'quick_key': trunk_system.quick_key,
                    'number_tag': trunk_system.number_tag,
                    'dqks_status': trunk_system.dqks_status,
                    'departments': []
                }

                # Export departments for this trunk system
                departments = CGroup.objects.using('favorites').filter(
                    trunk_system=trunk_system
                ).order_by('order')

                for dept in departments:
                    dept_data = {
                        'order': dept.order,
                        'name_tag': dept.name_tag,
                        'avoid': dept.avoid,
                        'latitude': str(dept.latitude) if dept.latitude else None,
                        'longitude': str(dept.longitude) if dept.longitude else None,
                        'range_miles': str(dept.range_miles) if dept.range_miles else None,
                        'location_type': dept.location_type,
                        'quick_key': dept.quick_key,
                        'filter': dept.filter,
                        'tgroups': []
                    }

                    # Export talk groups
                    tgroups = TGroup.objects.using('favorites').filter(
                        cgroup=dept
                    ).order_by('order')

                    for tgroup in tgroups:
                        tgroup_data = {
                            'order': tgroup.order,
                            'name_tag': tgroup.name_tag,
                            'avoid': tgroup.avoid,
                            'quick_key': tgroup.quick_key,
                            'tgids': []
                        }

                        # Export TGIDs
                        tgids = TGID.objects.using('favorites').filter(
                            tgroup=tgroup
                        ).order_by('order')

                        for tgid in tgids:
                            tgid_data = {
                                'order': tgid.order,
                                'name_tag': tgid.name_tag,
                                'avoid': tgid.avoid,
                                'tgid': tgid.tgid,
                                'quick_key': tgid.quick_key,
                                'priority': tgid.priority,
                            }
                            tgroup_data['tgids'].append(tgid_data)

                        dept_data['tgroups'].append(tgroup_data)

                    trunk_data['departments'].append(dept_data)

                fav_data['trunk_systems'].append(trunk_data)

            data['favorites_lists'].append(fav_data)

        return json.dumps(data, indent=2)

    @staticmethod
    def import_from_json(json_content: str) -> Tuple[int, List[str]]:
        """
        Import one or more Favourite Lists from JSON content
        Returns: (count of imported lists, list of errors)
        """
        errors = []
        imported_count = 0

        try:
            data = json.loads(json_content)

            if not isinstance(data, dict) or 'favorites_lists' not in data:
                errors.append('Invalid JSON format: missing favorites_lists key')
                return 0, errors

            filename_pattern = re.compile(r'^f_(\d{6})\.hpd$', re.IGNORECASE)
            existing_filenames = FavoritesList.objects.using('favorites').values_list('filename', flat=True)
            used_numbers = set()
            for filename in existing_filenames:
                match = filename_pattern.match(filename or '')
                if match:
                    used_numbers.add(int(match.group(1)))
            next_number = max(used_numbers or {0}) + 1

            for fav_list_data in data.get('favorites_lists', []):
                try:
                    while next_number in used_numbers:
                        next_number += 1
                    generated_filename = f"f_{next_number:06d}.hpd"
                    used_numbers.add(next_number)
                    next_number += 1

                    # Create or update the favorites list
                    fav_list, _ = FavoritesList.objects.using('favorites').get_or_create(
                        user_name=fav_list_data.get('user_name', 'Imported List'),
                        defaults={
                            'filename': generated_filename,
                            'scanner_model': fav_list_data.get('scanner_model', 'BCDx36HP'),
                            'format_version': fav_list_data.get('format_version', '1.00'),
                            'location_control': fav_list_data.get('location_control', 'Off'),
                            'monitor': fav_list_data.get('monitor', 'On'),
                            'quick_key': fav_list_data.get('quick_key', 'Off'),
                            'number_tag': fav_list_data.get('number_tag', 'Off'),
                        }
                    )

                    # Import conventional systems
                    for conv_idx, conv_data in enumerate(fav_list_data.get('conventional_systems', [])):
                        conv_system = ConventionalSystem.objects.using('favorites').create(
                            favorites_list=fav_list,
                            order=conv_data.get('order', conv_idx),
                            name_tag=conv_data.get('name_tag', ''),
                            avoid=conv_data.get('avoid', 'Off'),
                            system_type=conv_data.get('system_type', ''),
                            quick_key=conv_data.get('quick_key', 'Off'),
                            number_tag=conv_data.get('number_tag', 'Off'),
                            system_hold_time=conv_data.get('system_hold_time', 0),
                            analog_agc=conv_data.get('analog_agc', 'Off'),
                            digital_agc=conv_data.get('digital_agc', 'Off'),
                            digital_waiting_time=conv_data.get('digital_waiting_time', 400),
                            digital_threshold_mode=conv_data.get('digital_threshold_mode', 'Manual'),
                            digital_threshold_level=conv_data.get('digital_threshold_level', 8),
                            dqks_status=conv_data.get('dqks_status', []),
                        )

                        # Import groups and channels
                        for group_idx, group_data in enumerate(conv_data.get('groups', [])):
                            group = CGroup.objects.using('favorites').create(
                                conventional_system=conv_system,
                                order=group_data.get('order', group_idx),
                                name_tag=group_data.get('name_tag', ''),
                                avoid=group_data.get('avoid', 'Off'),
                                latitude=group_data.get('latitude'),
                                longitude=group_data.get('longitude'),
                                range_miles=group_data.get('range_miles'),
                                location_type=group_data.get('location_type', 'Circle'),
                                quick_key=group_data.get('quick_key', 'Off'),
                                filter=group_data.get('filter', ''),
                            )

                            # Import channels
                            for channel_idx, channel_data in enumerate(group_data.get('channels', [])):
                                CFreq.objects.using('favorites').create(
                                    cgroup=group,
                                    order=channel_data.get('order', channel_idx),
                                    name_tag=channel_data.get('name_tag', ''),
                                    avoid=channel_data.get('avoid', 'Off'),
                                    frequency=channel_data.get('frequency', 0),
                                    modulation=channel_data.get('modulation', 'AUTO'),
                                    audio_option=channel_data.get('audio_option', ''),
                                    func_tag_id=channel_data.get('func_tag_id', 0),
                                    attenuator=channel_data.get('attenuator', 'Off'),
                                    delay=channel_data.get('delay', 2),
                                    volume_offset=channel_data.get('volume_offset', 0),
                                    alert_tone=channel_data.get('alert_tone', 'Off'),
                                    alert_volume=channel_data.get('alert_volume', 'Auto'),
                                    alert_color=channel_data.get('alert_color', 'Off'),
                                    alert_pattern=channel_data.get('alert_pattern', 'On'),
                                    number_tag=channel_data.get('number_tag', 'Off'),
                                    priority_channel=channel_data.get('priority_channel', 'Off'),
                                )

                    # Import trunk systems
                    for trunk_idx, trunk_data in enumerate(fav_list_data.get('trunk_systems', [])):
                        trunk_system = TrunkSystem.objects.using('favorites').create(
                            favorites_list=fav_list,
                            order=trunk_data.get('order', trunk_idx),
                            name_tag=trunk_data.get('name_tag', ''),
                            system_type=trunk_data.get('system_type', 'P25Standard'),
                            avoid=trunk_data.get('avoid', 'Off'),
                            reserve=trunk_data.get('reserve', ''),
                            system_id_search=trunk_data.get('system_id_search', 'Srch'),
                            quick_key=trunk_data.get('quick_key', 'Off'),
                            number_tag=trunk_data.get('number_tag', 'Off'),
                            dqks_status=trunk_data.get('dqks_status', []),
                        )

                        # Import departments
                        for dept_idx, dept_data in enumerate(trunk_data.get('departments', [])):
                            dept = CGroup.objects.using('favorites').create(
                                trunk_system=trunk_system,
                                order=dept_data.get('order', dept_idx),
                                name_tag=dept_data.get('name_tag', ''),
                                avoid=dept_data.get('avoid', 'Off'),
                                latitude=dept_data.get('latitude'),
                                longitude=dept_data.get('longitude'),
                                range_miles=dept_data.get('range_miles'),
                                location_type=dept_data.get('location_type', 'Circle'),
                                quick_key=dept_data.get('quick_key', 'Off'),
                                filter=dept_data.get('filter', ''),
                            )

                            # Import talk groups
                            for tgroup_idx, tgroup_data in enumerate(dept_data.get('tgroups', [])):
                                tgroup = TGroup.objects.using('favorites').create(
                                    cgroup=dept,
                                    order=tgroup_data.get('order', tgroup_idx),
                                    name_tag=tgroup_data.get('name_tag', ''),
                                    avoid=tgroup_data.get('avoid', 'Off'),
                                    quick_key=tgroup_data.get('quick_key', 'Off'),
                                )

                                # Import TGIDs
                                for tgid_idx, tgid_data in enumerate(tgroup_data.get('tgids', [])):
                                    TGID.objects.using('favorites').create(
                                        tgroup=tgroup,
                                        order=tgid_data.get('order', tgid_idx),
                                        name_tag=tgid_data.get('name_tag', ''),
                                        avoid=tgid_data.get('avoid', 'Off'),
                                        tgid=tgid_data.get('tgid', 0),
                                        quick_key=tgid_data.get('quick_key', 'Off'),
                                        priority=tgid_data.get('priority', 'Any'),
                                    )

                    imported_count += 1

                except (ValueError, KeyError) as e:
                    errors.append(f"Error importing '{fav_list_data.get('user_name', 'Unknown')}': {str(e)}")

            return imported_count, errors

        except json.JSONDecodeError as e:
            errors.append(f"JSON parsing error: {str(e)}")
            return 0, errors
        except Exception as e:
            errors.append(f"Import error: {str(e)}")
            return 0, errors
