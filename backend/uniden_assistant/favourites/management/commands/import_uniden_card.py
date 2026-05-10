import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from uniden_assistant.favourites.favorites_hpd_parser import FavoritesHPDParser
from uniden_assistant.favourites.favorites_parser import FavoritesListParser
from uniden_assistant.favourites.models import FavoritesList, ScannerProfile
from uniden_assistant.favourites.parsers import UnidenFileParser


class Command(BaseCommand):
    help = "Import sample data from the data directory"

    @staticmethod
    def _resolve_favorites_dir(data_dir):
        direct_dir = data_dir / "favorites_lists"
        if direct_dir.exists():
            return direct_dir

        nested_dir = data_dir / "ubcdx36" / "favorites_lists"
        if nested_dir.exists():
            return nested_dir

        return nested_dir

    @staticmethod
    def _resolve_config_paths(data_dir):
        candidates = []
        for base_dir in (data_dir, data_dir / "ubcdx36"):
            candidates.extend([
                base_dir / "profile.cfg",
                base_dir / "app_data.cfg",
                base_dir / "scanner.inf",
                base_dir / "discvery.cfg",
            ])

        # Preserve order while removing duplicates when both base paths overlap.
        unique_paths = []
        seen_paths = set()
        for path in candidates:
            if path in seen_paths:
                continue
            seen_paths.add(path)
            unique_paths.append(path)
        return unique_paths

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

        favorites_dir = self._resolve_favorites_dir(data_dir)
        if options["favorites_only"]:
            hpd_files = sorted(favorites_dir.glob("*.hpd")) if favorites_dir.exists() else []
        else:
            hpd_files = sorted(data_dir.glob("**/*.hpd"))

        if not hpd_files:
            self.stderr.write(self.style.ERROR("No .hpd files found to import."))
            return

        parser = UnidenFileParser()
        imported = 0

        favorites_lookup = {}
        if favorites_dir.exists():
            flist_path = favorites_dir / "f_list.cfg"
            if flist_path.exists():
                try:
                    FavoritesListParser.parse_favorites_list(str(flist_path))
                    favorites_lookup = {
                        favorite.filename: favorite
                        for favorite in FavoritesList.objects.using('favorites').all()
                    }
                except Exception as exc:
                    self.stderr.write(self.style.WARNING(f"Failed to parse {flist_path}: {exc}"))

        for hpd_file in hpd_files:
            try:
                if hpd_file.parent == favorites_dir:
                    favorites_list = favorites_lookup.get(hpd_file.name)
                    if not favorites_list:
                        raise ValueError("No matching F-List entry found")
                    FavoritesHPDParser().parse_file(str(hpd_file), favorites_list)
                else:
                    profile_name = hpd_file.stem.replace("_", " ")
                    profile, _ = ScannerProfile.objects.get_or_create(
                        name=profile_name,
                        defaults={
                            "model": "Uniden",
                            "firmware_version": "",
                        },
                    )
                    with open(hpd_file, "rb") as f:
                        parser.parse(f, profile)
                imported += 1
            except Exception as exc:
                self.stderr.write(self.style.WARNING(f"Failed to import {hpd_file}: {exc}"))

        if not options["favorites_only"]:
            config_files = self._resolve_config_paths(data_dir)
            for cfg_path in config_files:
                if not cfg_path.exists():
                    continue
                try:
                    with open(cfg_path, "rb") as f:
                        parser.store_records_only(f)
                except Exception as exc:
                    self.stderr.write(self.style.WARNING(f"Failed to record {cfg_path}: {exc}"))

        self.stdout.write(self.style.SUCCESS(f"Imported {imported} profile(s)."))
