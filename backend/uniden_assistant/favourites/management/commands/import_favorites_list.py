"""Management command to import favorites list from f_list.cfg"""
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from uniden_assistant.favourites.favorites_parser import FavoritesListParser


class Command(BaseCommand):
    help = 'Import favorites list from f_list.cfg'

    def handle(self, *args, **options):
        favorites_dir = os.path.join(
            settings.UNIDEN_DATA_DIR, 
            'uniden', 
            'ubcdx36', 
            'favorites_lists'
        )
        
        if not os.path.exists(favorites_dir):
            self.stdout.write(self.style.ERROR(
                f'Favorites directory not found: {favorites_dir}'
            ))
            return
        
        flist_cfg = os.path.join(favorites_dir, 'f_list.cfg')
        
        if not os.path.exists(flist_cfg):
            self.stdout.write(self.style.ERROR(
                f'f_list.cfg not found: {flist_cfg}'
            ))
            return
        
        self.stdout.write('Parsing f_list.cfg...')
        FavoritesListParser.parse_favorites_list(flist_cfg)
        
        self.stdout.write(self.style.SUCCESS('Favorites list import completed!'))
