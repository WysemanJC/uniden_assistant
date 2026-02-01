from typing import Optional

HPDB_MODELS = {
    'country',
    'state',
    'county',
    'hpdbagency',
    'hpdbchannelgroup',
    'hpdbfrequency',
    'hpdbfilerecord',
    'hpdbrawfile',
    'hpdbrawline',
    'hpdbimportjob',
}

FAVORITES_MODELS = {
    'scannerprofile',
    'frequency',
    'channelgroup',
    'agency',
    'favoriteslist',
    'scannerfilerecord',
}

APPCONFIG_MODELS = {
    'scannermodel',
}


class UnidenDBRouter:
    """Route HPDB data to Mongo (hpdb), favorites to Mongo (favorites), Django core to SQLite."""

    def db_for_read(self, model, **hints) -> Optional[str]:
        model_name = model._meta.model_name
        if model._meta.app_label == 'appconfig' and model_name in APPCONFIG_MODELS:
            return 'appconfig'
        if model._meta.app_label == 'hpdb' and model_name in HPDB_MODELS:
            return 'hpdb'
        if model._meta.app_label == 'usersettings' and model_name in FAVORITES_MODELS:
            return 'favorites'
        return None

    def db_for_write(self, model, **hints) -> Optional[str]:
        model_name = model._meta.model_name
        if model._meta.app_label == 'appconfig' and model_name in APPCONFIG_MODELS:
            return 'appconfig'
        if model._meta.app_label == 'hpdb' and model_name in HPDB_MODELS:
            return 'hpdb'
        if model._meta.app_label == 'usersettings' and model_name in FAVORITES_MODELS:
            return 'favorites'
        return None

    def allow_relation(self, obj1, obj2, **hints) -> Optional[bool]:
        if obj1._meta.app_label == 'appconfig' and obj2._meta.app_label == 'appconfig':
            return True
        if obj1._meta.app_label == 'hpdb' and obj2._meta.app_label == 'hpdb':
            return True
        if obj1._meta.app_label == 'usersettings' and obj2._meta.app_label == 'usersettings':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints) -> Optional[bool]:
        if app_label == 'appconfig':
            return db == 'appconfig'
        if app_label == 'hpdb':
            return db == 'hpdb'
        if app_label == 'usersettings':
            return db == 'favorites'
        if app_label != 'hpdb' and app_label != 'usersettings':
            return db == 'default'

        model_name = (model_name or '').lower()
        if app_label == 'hpdb' and model_name in HPDB_MODELS:
            return db == 'hpdb'
        if app_label == 'usersettings' and model_name in FAVORITES_MODELS:
            return db == 'favorites'
        return None
