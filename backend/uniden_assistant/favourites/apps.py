from django.apps import AppConfig


class FavouritesConfig(AppConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = 'uniden_assistant.favourites'
