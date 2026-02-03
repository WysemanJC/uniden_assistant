import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from uniden_assistant.favourites.models import ScannerProfile
from uniden_assistant.favourites.parsers import UnidenFileParser


class Command(BaseCommand):
    help = "Import sample data from the data directory"

    def add_arguments(self, parser):
        parser.add_argument(
            "--data-dir",
            default=settings.UNIDEN_DATA_DIR,
            help="Path to data directory",
        )
        parser.add_argument(
            "--favorites-only",
            action="store_true",
            help="Import only favorites_lists/*.hpd",
        )

    def handle(self, *args, **options):
        data_dir = Path(options["data_dir"]).expanduser().resolve()
        if not data_dir.exists():
            self.stderr.write(self.style.ERROR(f"Data directory not found: {data_dir}"))
            return

        favorites_dir = data_dir / "ubcdx36" / "favorites_lists"
        if options["favorites_only"]:
            hpd_files = sorted(favorites_dir.glob("*.hpd")) if favorites_dir.exists() else []
        else:
            hpd_files = sorted(data_dir.glob("**/*.hpd"))

        if not hpd_files:
            self.stderr.write(self.style.ERROR("No .hpd files found to import."))
            return

        parser = UnidenFileParser()
        imported = 0

        for hpd_file in hpd_files:
            profile_name = hpd_file.stem.replace("_", " ")
            profile, _ = ScannerProfile.objects.get_or_create(
                name=profile_name,
                defaults={
                    "model": "Uniden",
                    "firmware_version": "",
                },
            )

            try:
                with open(hpd_file, "rb") as f:
                    parser.parse(f, profile)
                imported += 1
            except Exception as exc:
                self.stderr.write(self.style.WARNING(f"Failed to import {hpd_file}: {exc}"))

        if not options["favorites_only"]:
            config_files = [
                data_dir / "ubcdx36" / "profile.cfg",
                data_dir / "ubcdx36" / "app_data.cfg",
                data_dir / "ubcdx36" / "scanner.inf",
                data_dir / "ubcdx36" / "discvery.cfg",
            ]
            for cfg_path in config_files:
                if not cfg_path.exists():
                    continue
                try:
                    with open(cfg_path, "rb") as f:
                        parser.store_records_only(f)
                except Exception as exc:
                    self.stderr.write(self.style.WARNING(f"Failed to record {cfg_path}: {exc}"))

        self.stdout.write(self.style.SUCCESS(f"Imported {imported} profile(s)."))
