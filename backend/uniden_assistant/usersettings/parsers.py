"""
Parser for Uniden scanner configuration files
"""
import os
import re
from .models import Frequency, ChannelGroup, Agency, ScannerFileRecord
from uniden_assistant.record_parser.spec_field_maps import build_spec_field_map


class UnidenFileParser:
    """Parser for .hpd and .cfg files from Uniden scanners"""

    def parse(self, file, profile):
        """Parse a Uniden file and populate the profile"""
        content = file.read().decode('utf-8', errors='ignore')
        lines = content.split('\n')

        file_name = os.path.basename(getattr(file, 'name', '') or 'unknown')
        file_path = getattr(file, 'name', '') or ''

        self._store_records(lines, file_name, file_path)

        current_group = None

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split('\t')
            
            if parts[0] == 'TargetModel':
                profile.model = parts[1] if len(parts) > 1 else ''
            elif parts[0] == 'FormatVersion':
                continue
            elif parts[0] == 'C-Group':
                current_group = self._parse_channel_group(parts, profile)
            elif parts[0] == 'C-Freq':
                self._parse_frequency(parts, profile, current_group)
            elif parts[0] == 'Conventional':
                self._parse_agency(parts)

        profile.save()

    def _infer_file_path(self, file_path: str, file_name: str) -> str:
        """Infer relative file path for reconstruction."""
        if not file_path:
            return file_name

        normalized = file_path.replace('\\', '/')
        if '/favorites_lists/' in normalized:
            return 'favorites_lists/' + file_name
        if '/HPDB/' in normalized:
            return 'HPDB/' + file_name
        if normalized.endswith('/scanner.inf') or normalized.endswith('scanner.inf'):
            return 'scanner.inf'
        if normalized.endswith('/profile.cfg') or normalized.endswith('profile.cfg'):
            return 'profile.cfg'
        if normalized.endswith('/app_data.cfg') or normalized.endswith('app_data.cfg'):
            return 'app_data.cfg'
        if normalized.endswith('/discvery.cfg') or normalized.endswith('discvery.cfg'):
            return 'discvery.cfg'
        return file_name

    def _store_records(self, lines, file_name: str, file_path: str) -> None:
        records_buffer = []
        for idx, raw_line in enumerate(lines, start=1):
            raw_line = raw_line.rstrip('\r')
            if not raw_line:
                continue

            trailing_empty = len(raw_line) - len(raw_line.rstrip('\t'))
            parts = raw_line.split('\t')
            record_type = parts[0] if parts else ''
            fields = parts[1:] if len(parts) > 1 else []
            spec_field_order, spec_field_map = build_spec_field_map(record_type, fields)

            records_buffer.append(ScannerFileRecord(
                file_name=file_name,
                file_path=self._infer_file_path(file_path, file_name),
                record_type=record_type,
                fields=fields,
                spec_field_order=spec_field_order,
                spec_field_map=spec_field_map,
                trailing_empty_fields=trailing_empty,
                line_number=idx,
            ))

            if len(records_buffer) >= 2000:
                ScannerFileRecord.objects.bulk_create(records_buffer)
                records_buffer.clear()

        if records_buffer:
            ScannerFileRecord.objects.bulk_create(records_buffer)

    def store_records_only(self, file):
        """Store structured records for a file without parsing into models."""
        content = file.read().decode('utf-8', errors='ignore')
        lines = content.split('\n')
        file_name = os.path.basename(getattr(file, 'name', '') or 'unknown')
        file_path = getattr(file, 'name', '') or ''
        self._store_records(lines, file_name, file_path)

    def _parse_frequency(self, parts, profile, group=None):
        """Parse a frequency line (C-Freq)"""
        if len(parts) < 6:
            return

        items = parts[1:]
        while items and items[0] == '':
            items.pop(0)

        name = items[0] if len(items) > 0 else 'Unknown'
        enabled = items[1].lower() == 'on' if len(items) > 1 else True
        try:
            frequency = int(items[2]) if len(items) > 2 else 0
        except (ValueError, TypeError):
            frequency = 0
        modulation = items[3] if len(items) > 3 else 'AUTO'
        nac = items[4] if len(items) > 4 else ''

        if frequency > 0:
            freq_obj, created = Frequency.objects.get_or_create(
                profile=profile,
                frequency=frequency,
                defaults={
                    'name': name,
                    'modulation': modulation[:10],
                    'nac': nac.split('=')[1] if 'NAC=' in nac else '',
                    'enabled': enabled,
                }
            )
            if group is not None:
                group.frequencies.add(freq_obj)

    def _parse_channel_group(self, parts, profile):
        """Parse a channel group line (C-Group)"""
        if len(parts) < 3:
            return

        items = parts[1:]
        while items and items[0] == '':
            items.pop(0)

        name = items[0] if len(items) > 0 else 'Unknown'
        
        group, created = ChannelGroup.objects.get_or_create(
            profile=profile,
            name=name,
            defaults={'enabled': True}
        )

        return group

    def _parse_agency(self, parts):
        """Parse an agency line"""
        if len(parts) < 3:
            return

        agency_id = parts[1] if len(parts) > 1 else None
        name = parts[2] if len(parts) > 2 else 'Unknown'

        if agency_id:
            Agency.objects.get_or_create(
                agency_id=agency_id,
                defaults={'name': name}
            )

    def export(self, profile):
        """Export a profile to Uniden file format"""
        lines = [
            f'TargetModel\t{profile.model}',
            'FormatVersion\t1.00',
        ]

        # Export agencies
        for agency in Agency.objects.all():
            lines.append(f'Conventional\tAgencyId={agency.agency_id}\t\t{agency.name}\tOff')

        # Export channel groups and frequencies
        for group in profile.channel_groups.all():
            lines.append(f'C-Group\t\t{group.name}\tOff\t0.000000\t0.000000\t0.0\tCircle\tOff')

            for freq in group.frequencies.all():
                nac_str = f'NAC={freq.nac}' if freq.nac else ''
                enabled = 'On' if freq.enabled else 'Off'
                lines.append(f'C-Freq\t\t{freq.name}\t{enabled}\t{freq.frequency}\t{freq.modulation}\t{nac_str}\t208\tOff\t2\t0\tOff\tAuto\tOff\tOn\tOff\tOff')

        return '\n'.join(lines)
