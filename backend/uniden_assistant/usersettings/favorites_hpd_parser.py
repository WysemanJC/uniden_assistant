"""Parser for favorites f_*.hpd files (full record support)."""
from __future__ import annotations

import logging
from typing import Optional

from .models import (
    FavoritesList,
    ConventionalSystem,
    TrunkSystem,
    FleetMap,
    UnitId,
    AvoidTgid,
    CGroup,
    CFreq,
    Site,
    BandPlanP25,
    BandPlanMot,
    TFreq,
    TGroup,
    TGID,
    Rectangle,
    ScannerFileRecord,
)
from uniden_assistant.record_parser.spec_field_maps import build_spec_field_map

logger = logging.getLogger(__name__)


class FavoritesHPDParser:
    """Parse a favorites f_*.hpd file and store all record types."""

    def __init__(self) -> None:
        self.current_conventional: Optional[ConventionalSystem] = None
        self.current_cgroup: Optional[CGroup] = None
        self.current_trunk: Optional[TrunkSystem] = None
        self.current_site: Optional[Site] = None
        self.current_tgroup: Optional[TGroup] = None
        self.conventional_order = 0
        self.trunk_order = 0
        self.cgroup_order = 0
        self.cfreq_order = 0
        self.site_order = 0
        self.tfreq_order = 0
        self.tgroup_order = 0
        self.tgid_order = 0
        self.rectangle_order = 0
        self.fleetmap_order = 0
        self.unitid_order = 0
        self.avoid_tgid_order = 0

    def parse_file(self, file_path: str, favorites_list: FavoritesList) -> None:
        """Parse a favorites file into models."""
        self._reset_state()

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_number, raw_line in enumerate(f, start=1):
                raw_line = raw_line.rstrip('\n').rstrip('\r')
                if not raw_line:
                    continue

                parts_all = raw_line.split('\t')
                record_type = parts_all[0] if parts_all else ''
                fields = parts_all[1:] if len(parts_all) > 1 else []

                # Store structured record for reference
                self._store_record(file_path, record_type, fields, line_number, raw_line)

                if record_type == 'TargetModel':
                    favorites_list.scanner_model = fields[0] if fields else favorites_list.scanner_model
                    favorites_list.save(update_fields=['scanner_model'])
                    continue

                if record_type == 'FormatVersion':
                    favorites_list.format_version = fields[0] if fields else favorites_list.format_version
                    favorites_list.save(update_fields=['format_version'])
                    continue

                if record_type == 'Conventional':
                    self._parse_conventional(fields, favorites_list)
                    continue

                if record_type == 'Trunk':
                    self._parse_trunk(fields, favorites_list)
                    continue

                if record_type == 'DQKs_Status':
                    self._parse_dqks_status(fields)
                    continue

                if record_type == 'C-Group':
                    self._parse_cgroup(fields)
                    continue

                if record_type == 'C-Freq':
                    self._parse_cfreq(fields)
                    continue

                if record_type == 'Site':
                    self._parse_site(fields)
                    continue

                if record_type == 'BandPlan_P25':
                    self._parse_bandplan_p25(fields)
                    continue

                if record_type == 'BandPlan_Mot':
                    self._parse_bandplan_mot(fields)
                    continue

                if record_type == 'FleetMap':
                    self._parse_fleetmap(fields)
                    continue

                if record_type == 'UnitIds':
                    self._parse_unitids(fields)
                    continue

                if record_type == 'AvoidTgids':
                    self._parse_avoid_tgids(fields)
                    continue

                if record_type == 'T-Freq':
                    self._parse_tfreq(fields)
                    continue

                if record_type == 'T-Group':
                    self._parse_tgroup(fields)
                    continue

                if record_type == 'TGID':
                    self._parse_tgid(fields)
                    continue

                if record_type == 'Rectangle':
                    self._parse_rectangle(fields)
                    continue

    def _reset_state(self) -> None:
        self.current_conventional = None
        self.current_cgroup = None
        self.current_trunk = None
        self.current_site = None
        self.current_tgroup = None
        self.conventional_order = 0
        self.trunk_order = 0
        self.cgroup_order = 0
        self.cfreq_order = 0
        self.site_order = 0
        self.tfreq_order = 0
        self.tgroup_order = 0
        self.tgid_order = 0
        self.rectangle_order = 0
        self.fleetmap_order = 0
        self.unitid_order = 0
        self.avoid_tgid_order = 0

    def _store_record(self, file_path: str, record_type: str, fields: list[str], line_number: int, raw_line: str) -> None:
        trailing_empty = len(raw_line) - len(raw_line.rstrip('\t'))
        spec_field_order, spec_field_map = build_spec_field_map(record_type, fields)
        ScannerFileRecord.objects.using('favorites').create(
            file_name=file_path.split('/')[-1],
            file_path='favorites_lists/' + file_path.split('/')[-1],
            record_type=record_type,
            fields=fields,
            spec_field_order=spec_field_order,
            spec_field_map=spec_field_map,
            trailing_empty_fields=trailing_empty,
            line_number=line_number,
        )

    def _parse_conventional(self, fields: list[str], favorites_list: FavoritesList) -> None:
        # Don't trim - keep field positions per spec
        if not fields:
            return

        self.current_conventional = ConventionalSystem.objects.using('favorites').create(
            favorites_list=favorites_list,
            my_id=fields[0] if len(fields) > 0 else '',
            parent_id=fields[1] if len(fields) > 1 else '',
            name_tag=fields[2] if len(fields) > 2 else '',
            avoid=fields[3] if len(fields) > 3 else 'Off',
            reserve=fields[4] if len(fields) > 4 else '',
            system_type=fields[5] if len(fields) > 5 else '',
            quick_key=fields[6] if len(fields) > 6 else 'Off',
            number_tag=fields[7] if len(fields) > 7 else 'Off',
            system_hold_time=int(fields[8]) if len(fields) > 8 and fields[8].isdigit() else 0,
            analog_agc=fields[9] if len(fields) > 9 else 'Off',
            digital_agc=fields[10] if len(fields) > 10 else 'Off',
            digital_waiting_time=int(fields[11]) if len(fields) > 11 and fields[11].isdigit() else 400,
            digital_threshold_mode=fields[12] if len(fields) > 12 else 'Manual',
            digital_threshold_level=int(fields[13]) if len(fields) > 13 and fields[13].isdigit() else 8,
            order=self.conventional_order,
        )
        self.conventional_order += 1
        self.current_trunk = None
        self.current_site = None
        self.current_tgroup = None
        self.current_cgroup = None
        self.cgroup_order = 0
        self.cfreq_order = 0
        self.rectangle_order = 0

    def _parse_trunk(self, fields: list[str], favorites_list: FavoritesList) -> None:
        # Don't trim - keep field positions per spec
        if not fields:
            return

        self.current_trunk = TrunkSystem.objects.using('favorites').create(
            favorites_list=favorites_list,
            my_id=fields[0] if len(fields) > 0 else '',
            parent_id=fields[1] if len(fields) > 1 else '',
            name_tag=fields[2] if len(fields) > 2 else '',
            avoid=fields[3] if len(fields) > 3 else 'Off',
            reserve=fields[4] if len(fields) > 4 else '',
            system_type=fields[5] if len(fields) > 5 else '',
            id_search=fields[6] if len(fields) > 6 else 'Off',
            alert_tone=fields[7] if len(fields) > 7 else 'Off',
            alert_volume=fields[8] if len(fields) > 8 else 'Auto',
            status_bit=fields[9] if len(fields) > 9 else 'Ignore',
            nac=fields[10] if len(fields) > 10 else 'Srch',
            quick_key=fields[11] if len(fields) > 11 else 'Off',
            number_tag=fields[12] if len(fields) > 12 else 'Off',
            site_hold_time=int(fields[13]) if len(fields) > 13 and fields[13].isdigit() else 0,
            analog_agc=fields[14] if len(fields) > 14 else 'Off',
            digital_agc=fields[15] if len(fields) > 15 else 'Off',
            end_code=fields[16] if len(fields) > 16 else 'Analog',
            priority_id_scan=fields[17] if len(fields) > 17 else 'Off',
            alert_color=fields[18] if len(fields) > 18 else 'Off',
            alert_pattern=fields[19] if len(fields) > 19 else 'On',
            tgid_format=fields[20] if len(fields) > 20 else '',
            order=self.trunk_order,
        )
        self.trunk_order += 1
        self.current_conventional = None
        self.current_site = None
        self.current_tgroup = None
        self.current_cgroup = None
        self.site_order = 0
        self.tfreq_order = 0
        self.tgroup_order = 0
        self.tgid_order = 0
        self.rectangle_order = 0
        self.fleetmap_order = 0
        self.unitid_order = 0
        self.avoid_tgid_order = 0

    def _parse_dqks_status(self, fields: list[str]) -> None:
        items = self._trim_leading_empty(fields)
        if not items:
            return

        my_id = items[0] if len(items) > 0 else ''
        flags = items[1:] if len(items) > 1 else []

        if self.current_conventional:
            self.current_conventional.dqks_my_id = my_id
            self.current_conventional.dqks_status = flags
            self.current_conventional.save(update_fields=['dqks_my_id', 'dqks_status'])
            return

        if self.current_trunk:
            self.current_trunk.dqks_my_id = my_id
            self.current_trunk.dqks_status = flags
            self.current_trunk.save(update_fields=['dqks_my_id', 'dqks_status'])

    def _parse_cgroup(self, fields: list[str]) -> None:
        if not self.current_conventional:
            return
        if not fields:
            return

        self.current_cgroup = CGroup.objects.using('favorites').create(
            conventional_system=self.current_conventional,
            my_id=fields[0] if len(fields) > 0 else '',
            parent_id=fields[1] if len(fields) > 1 else '',
            name_tag=fields[2] if len(fields) > 2 else '',
            avoid=fields[3] if len(fields) > 3 else 'Off',
            latitude=self._to_decimal(fields[4]) if len(fields) > 4 else None,
            longitude=self._to_decimal(fields[5]) if len(fields) > 5 else None,
            range_miles=self._to_decimal(fields[6]) if len(fields) > 6 else None,
            location_type=fields[7] if len(fields) > 7 else 'Circle',
            quick_key=fields[8] if len(fields) > 8 else 'Off',
            filter=fields[9] if len(fields) > 9 else '',
            order=self.cgroup_order,
        )
        self.cgroup_order += 1
        self.cfreq_order = 0
        self.rectangle_order = 0

    def _parse_cfreq(self, fields: list[str]) -> None:
        if not self.current_cgroup:
            return
        if not fields:
            return

        CFreq.objects.using('favorites').create(
            cgroup=self.current_cgroup,
            my_id=fields[0] if len(fields) > 0 else '',
            parent_id=fields[1] if len(fields) > 1 else '',
            name_tag=fields[2] if len(fields) > 2 else '',
            avoid=fields[3] if len(fields) > 3 else 'Off',
            frequency=int(fields[4]) if len(fields) > 4 and fields[4].isdigit() else 0,
            modulation=fields[5] if len(fields) > 5 else 'AUTO',
            audio_option=fields[6] if len(fields) > 6 else '',
            func_tag_id=int(fields[7]) if len(fields) > 7 and fields[7].isdigit() else 0,
            attenuator=fields[8] if len(fields) > 8 else 'Off',
            delay=int(fields[9]) if len(fields) > 9 and self._is_int(fields[9]) else 2,
            volume_offset=int(fields[10]) if len(fields) > 10 and self._is_int(fields[10]) else 0,
            alert_tone=fields[11] if len(fields) > 11 else 'Off',
            alert_volume=fields[12] if len(fields) > 12 else 'Auto',
            alert_color=fields[13] if len(fields) > 13 else 'Off',
            alert_pattern=fields[14] if len(fields) > 14 else 'On',
            number_tag=fields[15] if len(fields) > 15 else 'Off',
            priority_channel=fields[16] if len(fields) > 16 else 'Off',
            order=self.cfreq_order,
        )
        self.cfreq_order += 1

    def _parse_site(self, fields: list[str]) -> None:
        if not self.current_trunk:
            return
        items = self._trim_leading_empty(fields)
        if not items:
            return

        self.current_site = Site.objects.using('favorites').create(
            trunk_system=self.current_trunk,
            my_id=items[0] if len(items) > 0 else '',
            parent_id=items[1] if len(items) > 1 else '',
            name_tag=items[2] if len(items) > 2 else '',
            avoid=items[3] if len(items) > 3 else 'Off',
            latitude=self._to_decimal(items[4]) if len(items) > 4 else None,
            longitude=self._to_decimal(items[5]) if len(items) > 5 else None,
            range_miles=self._to_decimal(items[6]) if len(items) > 6 else None,
            modulation=items[7] if len(items) > 7 else 'AUTO',
            mot_band_type=items[8] if len(items) > 8 else 'Standard',
            edacs_band_type=items[9] if len(items) > 9 else 'Wide',
            location_type=items[10] if len(items) > 10 else 'Circle',
            attenuator=items[11] if len(items) > 11 else 'Off',
            digital_waiting_time=int(items[12]) if len(items) > 12 and items[12].isdigit() else 400,
            digital_threshold_mode=items[13] if len(items) > 13 else 'Manual',
            digital_threshold_level=int(items[14]) if len(items) > 14 and items[14].isdigit() else 8,
            quick_key=items[15] if len(items) > 15 else 'Off',
            nac=items[16] if len(items) > 16 else 'Srch',
            filter=items[17] if len(items) > 17 else '',
            order=self.site_order,
        )
        self.site_order += 1
        self.current_tgroup = None
        self.tfreq_order = 0
        self.rectangle_order = 0

    def _parse_bandplan_p25(self, fields: list[str]) -> None:
        if not self.current_site:
            return
        items = self._trim_leading_empty(fields)
        if not items:
            return

        my_id = items[0] if len(items) > 0 else ''
        band_plan = {}
        values = items[1:]
        for idx in range(0, len(values), 2):
            band_index = idx // 2
            base = values[idx] if idx < len(values) else ''
            spacing = values[idx + 1] if idx + 1 < len(values) else ''
            band_plan[str(band_index)] = {
                'base': int(base) if base.isdigit() else 0,
                'spacing': int(spacing) if spacing.isdigit() else 0,
            }

        BandPlanP25.objects.using('favorites').update_or_create(
            site=self.current_site,
            defaults={'band_plan': band_plan}
        )

    def _parse_bandplan_mot(self, fields: list[str]) -> None:
        if not self.current_site:
            return
        items = self._trim_leading_empty(fields)
        if not items:
            return

        my_id = items[0] if len(items) > 0 else ''
        band_plan = {}
        values = items[1:]
        for idx in range(0, len(values), 4):
            band_index = idx // 4
            lower = values[idx] if idx < len(values) else ''
            upper = values[idx + 1] if idx + 1 < len(values) else ''
            spacing = values[idx + 2] if idx + 2 < len(values) else ''
            offset = values[idx + 3] if idx + 3 < len(values) else ''
            band_plan[str(band_index)] = {
                'lower': int(lower) if lower.isdigit() else 0,
                'upper': int(upper) if upper.isdigit() else 0,
                'spacing': int(spacing) if spacing.isdigit() else 0,
                'offset': int(offset) if self._is_int(offset) else 0,
            }

        BandPlanMot.objects.using('favorites').update_or_create(
            site=self.current_site,
            defaults={'band_plan': band_plan}
        )

    def _parse_tfreq(self, fields: list[str]) -> None:
        if not self.current_site:
            return
        items = self._trim_leading_empty(fields)
        if not items:
            return

        TFreq.objects.using('favorites').create(
            site=self.current_site,
            reserve_my_id=items[0] if len(items) > 0 else '',
            parent_id=items[1] if len(items) > 1 else '',
            reserve1=items[2] if len(items) > 2 else '',
            reserve_avoid=items[3] if len(items) > 3 else 'Off',
            frequency=int(items[4]) if len(items) > 4 and items[4].isdigit() else 0,
            lcn=int(items[5]) if len(items) > 5 and items[5].isdigit() else 0,
            color_code_ran_area=items[6] if len(items) > 6 else '',
            order=self.tfreq_order,
        )
        self.tfreq_order += 1

    def _parse_tgroup(self, fields: list[str]) -> None:
        if not self.current_trunk:
            return
        if not fields:
            return

        self.current_tgroup = TGroup.objects.using('favorites').create(
            trunk_system=self.current_trunk,
            my_id=fields[0] if len(fields) > 0 else '',
            parent_id=fields[1] if len(fields) > 1 else '',
            name_tag=fields[2] if len(fields) > 2 else '',
            avoid=fields[3] if len(fields) > 3 else 'Off',
            latitude=self._to_decimal(fields[4]) if len(fields) > 4 else None,
            longitude=self._to_decimal(fields[5]) if len(fields) > 5 else None,
            range_miles=self._to_decimal(fields[6]) if len(fields) > 6 else None,
            location_type=fields[7] if len(fields) > 7 else 'Circle',
            quick_key=fields[8] if len(fields) > 8 else 'Off',
            order=self.tgroup_order,
        )
        self.tgroup_order += 1
        self.tgid_order = 0
        self.rectangle_order = 0

    def _parse_tgid(self, fields: list[str]) -> None:
        if not self.current_tgroup:
            return
        if not fields:
            return

        TGID.objects.using('favorites').create(
            tgroup=self.current_tgroup,
            my_id=fields[0] if len(fields) > 0 else '',
            parent_id=fields[1] if len(fields) > 1 else '',
            name_tag=fields[2] if len(fields) > 2 else '',
            avoid=fields[3] if len(fields) > 3 else 'Off',
            tgid=fields[4] if len(fields) > 4 else '',
            audio_type=fields[5] if len(fields) > 5 else 'ALL',
            func_tag_id=int(fields[6]) if len(fields) > 6 and fields[6].isdigit() else 0,
            delay=int(fields[7]) if len(fields) > 7 and self._is_int(fields[7]) else 2,
            volume_offset=int(fields[8]) if len(fields) > 8 and self._is_int(fields[8]) else 0,
            alert_tone=fields[9] if len(fields) > 9 else 'Off',
            alert_volume=fields[10] if len(fields) > 10 else 'Auto',
            alert_color=fields[11] if len(fields) > 11 else 'Off',
            alert_pattern=fields[12] if len(fields) > 12 else 'On',
            number_tag=fields[13] if len(fields) > 13 else 'Off',
            priority_channel=fields[14] if len(fields) > 14 else 'Off',
            tdma_slot=fields[15] if len(fields) > 15 else 'Any',
            order=self.tgid_order,
        )
        self.tgid_order += 1

    def _parse_rectangle(self, fields: list[str]) -> None:
        items = self._trim_leading_empty(fields)
        if len(items) < 5:
            return

        rectangle_data = {
            'my_id': items[0],
            'latitude1': self._to_decimal(items[1]),
            'longitude1': self._to_decimal(items[2]),
            'latitude2': self._to_decimal(items[3]),
            'longitude2': self._to_decimal(items[4]),
            'order': self.rectangle_order,
        }

        if self.current_site:
            Rectangle.objects.using('favorites').create(site=self.current_site, **rectangle_data)
            return

        if self.current_tgroup:
            Rectangle.objects.using('favorites').create(tgroup=self.current_tgroup, **rectangle_data)
            return

        if self.current_cgroup:
            Rectangle.objects.using('favorites').create(cgroup=self.current_cgroup, **rectangle_data)
            self.rectangle_order += 1

    def _parse_fleetmap(self, fields: list[str]) -> None:
        if not self.current_trunk:
            return
        items = self._trim_leading_empty(fields)
        if not items:
            return

        my_id = items[0] if len(items) > 0 else ''
        blocks = items[1:9] if len(items) > 1 else []
        FleetMap.objects.using('favorites').create(
            trunk_system=self.current_trunk,
            my_id=my_id,
            blocks=blocks,
            order=self.fleetmap_order,
        )
        self.fleetmap_order += 1

    def _parse_unitids(self, fields: list[str]) -> None:
        if not self.current_trunk:
            return
        items = self._trim_leading_empty(fields)
        if len(items) < 4:
            return

        UnitId.objects.using('favorites').create(
            trunk_system=self.current_trunk,
            reserve1=items[0] if len(items) > 0 else '',
            reserve2=items[1] if len(items) > 1 else '',
            name_tag=items[2] if len(items) > 2 else '',
            unit_id=int(items[3]) if len(items) > 3 and items[3].isdigit() else 0,
            alert_tone=items[4] if len(items) > 4 else 'Off',
            alert_volume=items[5] if len(items) > 5 else 'Auto',
            alert_color=items[6] if len(items) > 6 else 'Off',
            alert_pattern=items[7] if len(items) > 7 else 'On',
            order=self.unitid_order,
        )
        self.unitid_order += 1

    def _parse_avoid_tgids(self, fields: list[str]) -> None:
        if not self.current_trunk:
            return
        items = self._trim_leading_empty(fields)
        if not items:
            return

        my_id = items[0] if len(items) > 0 else ''
        tgids = items[1:] if len(items) > 1 else []
        AvoidTgid.objects.using('favorites').create(
            trunk_system=self.current_trunk,
            my_id=my_id,
            tgids=tgids,
            order=self.avoid_tgid_order,
        )
        self.avoid_tgid_order += 1

    @staticmethod
    def _trim_leading_empty(items: list[str]) -> list[str]:
        while items and items[0] == '':
            items = items[1:]
        return items

    @staticmethod
    def _to_decimal(value: str):
        try:
            return float(value) if value != '' else None
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _is_int(value: str) -> bool:
        try:
            int(value)
            return True
        except (ValueError, TypeError):
            return False
