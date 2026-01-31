"""Management command to import HPDB database from SD Card"""
import os
import glob
from django.core.management.base import BaseCommand
from django.conf import settings
from uniden_assistant.hpdb.hpdb_parser import HPDBParser


class Command(BaseCommand):
    help = 'Import HPDB database from ubcdx36/HPDB folder'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Limit number of system files to import (for testing)'
        )

    def handle(self, *args, **options):
        hpdb_dir = os.path.join(settings.UNIDEN_DATA_DIR, 'ubcdx36', 'HPDB')
        
        if not os.path.exists(hpdb_dir):
            self.stdout.write(self.style.ERROR(f'HPDB directory not found: {hpdb_dir}'))
            return
        
        hpdb_cfg = os.path.join(hpdb_dir, 'hpdb.cfg')
        
        if not os.path.exists(hpdb_cfg):
            self.stdout.write(self.style.ERROR(f'hpdb.cfg not found: {hpdb_cfg}'))
            return
        
        parser = HPDBParser()
        
        # Parse hpdb.cfg first to get states and counties
        self.stdout.write('Parsing hpdb.cfg...')
        parser.parse_hpdb_cfg(hpdb_cfg)
        self.stdout.write(self.style.SUCCESS(
            f'Parsed {len(parser.states)} states and {len(parser.counties)} counties'
        ))
        
        # Find all s_*.hpd files
        system_files = glob.glob(os.path.join(hpdb_dir, 's_*.hpd'))
        system_files.sort()
        
        limit = options.get('limit')
        if limit:
            system_files = system_files[:limit]
            self.stdout.write(f'Limited to {limit} system files')
        
        self.stdout.write(f'Found {len(system_files)} system files to import')
        
        # Parse each system file
        for i, file_path in enumerate(system_files, 1):
            filename = os.path.basename(file_path)
            self.stdout.write(f'[{i}/{len(system_files)}] Parsing {filename}...')
            parser.parse_system_file(file_path)
        
        self.stdout.write(self.style.SUCCESS('HPDB import completed!'))
