from django.apps import AppConfig


class AppConfigConfig(AppConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = 'uniden_assistant.appconfig'
    label = 'appconfig'
