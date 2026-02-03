"""Import favorites f_*.hpd files into full favorites models."""
import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from uniden_assistant.favourites.models import FavoritesList
from uniden_assistant.favourites.favorites_hpd_parser import FavoritesHPDParser


class Command(BaseCommand):
    help = "Import favorites f_*.hpd files into full favorites models"

    def add_arguments(self, parser):
        parser.add_argument(
            "--data-dir",
            default=settings.UNIDEN_DATA_DIR,
            help="Path to data directory",
        )

    def handle(self, *args, **options):
        data_dir = Path(options["data_dir"]).expanduser().resolve()
        favorites_dir = data_dir / "ubcdx36" / "favorites_lists"

        if not favorites_dir.exists():
            self.stderr.write(self.style.ERROR(f"Favorites directory not found: {favorites_dir}"))
            return

        hpd_files = sorted(favorites_dir.glob("f_*.hpd"))
        if not hpd_files:
            self.stderr.write(self.style.ERROR("No f_*.hpd files found to import."))
            return

        parser = FavoritesHPDParser()
        imported = 0

        for hpd_file in hpd_files:
            filename = hpd_file.name
            favorites_list, _ = FavoritesList.objects.get_or_create(
                filename=filename,
                defaults={
                    "user_name": filename,
                    "location_control": "Off",
                    "monitor": "Off",
                    "quick_key": "Off",
                    "number_tag": "Off",
                    "startup_keys": [],
                    "s_qkeys": [],
                },
            )

            try:
                parser.parse_file(str(hpd_file), favorites_list)
                imported += 1
            except Exception as exc:
                self.stderr.write(self.style.WARNING(f"Failed to import {hpd_file}: {exc}"))

        self.stdout.write(self.style.SUCCESS(f"Imported {imported} favorites file(s)."))
