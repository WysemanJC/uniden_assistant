from typing import Optional

FAVORITES_MODELS = {
    'scannerprofile',
    'frequency',
    'channelgroup',
    'agency',
    'favoriteslist',
    'scannerfilerecord',
    # New hierarchical favorites models
    'conventionalsystem',
    'trunksystem',
    'cgroup',
    'cfreq',
    'site',
    'bandplanp25',
    'bandplanmot',
    'tfreq',
    'tgroup',
    'tgid',
    'rectangle',
    'fleetmap',
    'unitid',
    'avoidtgid',
}


class UnidenDBRouter:
    """Route favorites to Mongo (favorites), Django core to SQLite."""

    def db_for_read(self, model, **hints) -> Optional[str]:
        model_name = model._meta.model_name
        if model._meta.app_label == 'favourites' and model_name in FAVORITES_MODELS:
            return 'favorites'
        return None

    def db_for_write(self, model, **hints) -> Optional[str]:
        model_name = model._meta.model_name
        if model._meta.app_label == 'favourites' and model_name in FAVORITES_MODELS:
            return 'favorites'
        return None

    def allow_relation(self, obj1, obj2, **hints) -> Optional[bool]:
        if obj1._meta.app_label == 'favourites' and obj2._meta.app_label == 'favourites':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints) -> Optional[bool]:
        if app_label == 'favourites':
            return db == 'favorites'
        if app_label != 'favourites':
            return db == 'default'

        model_name = (model_name or '').lower()
        if app_label == 'favourites' and model_name in FAVORITES_MODELS:
            return db == 'favorites'
        return None
