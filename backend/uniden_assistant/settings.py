"""
Django settings for uniden_assistant project.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def get_env(key, default=None):
    value = os.environ.get(key)
    if value is None:
        return default
    value = value.strip()
    if value == '':
        return default
    return value


def get_env_bool(key, default=False):
    value = get_env(key)
    if value is None:
        return default
    return value.lower() in {'1', 'true', 'yes', 'on'}


def get_env_list(key, default=''):
    value = get_env(key, default)
    if not value:
        return []
    return [item.strip() for item in value.split(',') if item.strip()]


def get_env_path(key, default):
    return Path(get_env(key, default)).expanduser()


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env('SECRET_KEY', default='django-insecure-dev-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_env_bool('DEBUG', default=False)

# EXTERNAL_URL: single env var for the public URL of this deployment.
# e.g. https://uniden.homeofdata.com  or  http://192.168.1.10:8080
# All of ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS, and CORS_ALLOWED_ORIGINS are
# derived from it automatically. The individual env vars still work as overrides.
_external_url = get_env('EXTERNAL_URL', default='')
_external_host = ''
if _external_url:
    from urllib.parse import urlparse as _urlparse
    _parsed = _urlparse(_external_url)
    _external_host = _parsed.hostname or ''

# ALLOWED_HOSTS — always includes loopback for the internal proxy
_allowed_hosts_env = get_env_list('ALLOWED_HOSTS', default='')
ALLOWED_HOSTS = _allowed_hosts_env if _allowed_hosts_env else (
    [_external_host] if _external_host else ['localhost', '127.0.0.1', '[::1]']
)
for _loopback in ('127.0.0.1', 'localhost', '[::1]'):
    if _loopback not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_loopback)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'uniden_assistant.favourites',
    'uniden_assistant.uniden_manager',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'uniden_assistant.urls_main'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'uniden_assistant.wsgi.application'

# Database
UNIDEN_DATA_DIR = get_env_path('UNIDEN_DATA_DIR', default='/data/uniden_assistant')
UNIDEN_DB_DIR = get_env_path('UNIDEN_DB_DIR', default=str(UNIDEN_DATA_DIR / 'db'))
FAVOURITES_DB_PATH = UNIDEN_DB_DIR / 'uniden_assistant_favourites.sqlite3'
DEFAULT_DB_PATH = UNIDEN_DB_DIR / 'uniden_assistant.sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DEFAULT_DB_PATH,
        'OPTIONS': {
            'timeout': 30,  # Retry SQLITE_BUSY for up to 30 seconds (important on NAS volumes)
        },
    },
    'favorites': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': FAVOURITES_DB_PATH,
        'OPTIONS': {
            'timeout': 30,  # Retry SQLITE_BUSY for up to 30 seconds (important on NAS volumes)
        },
    },
}

DATABASE_ROUTERS = ['uniden_assistant.db_router.UnidenDBRouter']

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Media files
MEDIA_URL = '/media/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# Reverse proxy / HTTPS settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = get_env_bool('USE_X_FORWARDED_HOST', default=False)

# CORS / CSRF — derived from EXTERNAL_URL, overridable individually
_csrf_env = get_env_list('CSRF_TRUSTED_ORIGINS', default='')
CSRF_TRUSTED_ORIGINS = _csrf_env if _csrf_env else ([_external_url] if _external_url else [])

_cors_env = get_env_list('CORS_ALLOWED_ORIGINS', default='')
CORS_ALLOW_ALL_ORIGINS = get_env_bool('CORS_ALLOW_ALL_ORIGINS', default=False)
CORS_ALLOWED_ORIGINS = _cors_env if _cors_env else ([_external_url] if _external_url else [])
CORS_ALLOW_CREDENTIALS = get_env_bool('CORS_ALLOW_CREDENTIALS', default=True)

# File upload settings
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_NUMBER_FILES = 10000  # Allow up to 10,000 files per upload
MEDIA_ROOT = get_env_path('MEDIA_ROOT', default=str(UNIDEN_DATA_DIR / 'media'))
STATIC_ROOT = get_env_path('STATIC_ROOT', default=str(BASE_DIR / 'staticfiles'))

# Logging
UNIDEN_LOG_DIR = get_env_path('UNIDEN_LOG_DIR', default=str(UNIDEN_DATA_DIR / 'logs' / 'backend'))
UNIDEN_LOG_DIR.mkdir(parents=True, exist_ok=True)
DJANGO_LOG_FILE = UNIDEN_LOG_DIR / 'django.log'
DJANGO_REQUEST_LOG_FILE = UNIDEN_LOG_DIR / 'django-requests.log'
APP_LOG_LEVEL = get_env('LOG_LEVEL', get_env('APP_LOG_LEVEL', 'DEBUG' if DEBUG else 'INFO'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s [%(name)s] %(message)s'
        },
        'simple': {
            'format': '%(levelname)s [%(name)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'backend_file': {
            'class': 'logging.FileHandler',
            'filename': str(DJANGO_LOG_FILE),
            'formatter': 'verbose',
        },
        'request_file': {
            'class': 'logging.FileHandler',
            'filename': str(DJANGO_REQUEST_LOG_FILE),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'backend_file'],
            'level': get_env('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'request_file'],
            'level': get_env('DJANGO_REQUEST_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'uniden_assistant': {
            'handlers': ['console', 'backend_file'],
            'level': APP_LOG_LEVEL,
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console', 'backend_file'],
        'level': get_env('ROOT_LOG_LEVEL', 'INFO'),
    },
}
