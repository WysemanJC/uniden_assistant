"""
Django settings for uniden_assistant project.
"""

import os
from pathlib import Path
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

def find_config_env(start: Path) -> Path:
    """Find config.env by walking up from the given path."""
    for candidate_root in [start, *start.parents]:
        candidate = candidate_root / 'config.env'
        if candidate.exists():
            return candidate
    raise RuntimeError("config.env not found in any parent directory")

# Load config.env from workspace root (required)
ENV_PATH = find_config_env(BASE_DIR)
ENV_VARS = {}

def load_env(path: Path) -> None:
    if not path.exists():
        return
    with path.open('r', encoding='utf-8') as fh:
        for raw_line in fh:
            line = raw_line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            ENV_VARS[key] = value
            os.environ[key] = value

load_env(ENV_PATH)

def get_setting(key, default=None, cast=None):
    value = ENV_VARS.get(key, os.environ.get(key, default))
    if cast is not None and value is not None:
        return cast(value)
    return value

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_setting('SECRET_KEY', default='django-insecure-dev-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_setting('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = get_setting('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

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
    'uniden_assistant.hpdb',
    'uniden_assistant.usersettings',
    'uniden_assistant.uniden_manager',
    'uniden_assistant.appconfig',
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
HPDB_MONGO_USER = get_setting('UNIDEN_HPDB_DB_USER', default='')
HPDB_MONGO_PASSWORD = get_setting('UNIDEN_HPDB_DB_PASSWORD', default='')
USERSETTINGS_MONGO_USER = get_setting('UNIDEN_USERSETTINGS_DB_USER', default='')
USERSETTINGS_MONGO_PASSWORD = get_setting('UNIDEN_USERSETTINGS_DB_PASSWORD', default='')
APPCONFIG_MONGO_USER = get_setting('UNIDEN_APP_DB_USER', default='')
APPCONFIG_MONGO_PASSWORD = get_setting('UNIDEN_APP_DB_PASSWORD', default='')

HPDB_DB_URI = get_setting('UNIDEN_HPDB_DB')
USERSETTINGS_DB_URI = get_setting('UNIDEN_USERSETTINGS_DB')
APPCONFIG_DB_URI = get_setting('UNIDEN_APP_DB')

missing_uris = [
    key for key, value in (
        ('UNIDEN_HPDB_DB', HPDB_DB_URI),
        ('UNIDEN_USERSETTINGS_DB', USERSETTINGS_DB_URI),
        ('UNIDEN_APP_DB', APPCONFIG_DB_URI),
    ) if not value
]
if missing_uris:
    raise RuntimeError(
        f"Missing MongoDB URI(s): {', '.join(missing_uris)}. "
        f"Check {ENV_PATH}"
    )

def _reject_localhost(uri: str, key: str) -> None:
    if 'localhost' in uri or '127.0.0.1' in uri:
        raise RuntimeError(
            f"{key} points to localhost. Refusing to start. Check {ENV_PATH}"
        )

def _ensure_direct_connection(uri: str) -> str:
    """Add directConnection=true to MongoDB URI"""
    parsed = urlparse(uri)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    if query.get('directConnection', '').lower() != 'true':
        query['directConnection'] = 'true'
    new_query = urlencode(query)
    return urlunparse(parsed._replace(query=new_query))

def _force_ipv4(uri: str) -> str:
    """Replace hostname with IPv4 address to avoid WSL IPv6 issues"""
    import socket
    parsed = urlparse(uri)
    hostname = parsed.hostname
    port = parsed.port or 27017
    
    try:
        # Get IPv4 address only
        ipv4_addr = socket.getaddrinfo(hostname, port, socket.AF_INET)[0][4][0]
        # Replace hostname with IPv4 address in netloc
        new_netloc = parsed.netloc.replace(hostname, ipv4_addr)
        return urlunparse(parsed._replace(netloc=new_netloc))
    except (socket.gaierror, IndexError):
        # If resolution fails, return original URI
        return uri

_reject_localhost(HPDB_DB_URI, 'UNIDEN_HPDB_DB')
_reject_localhost(USERSETTINGS_DB_URI, 'UNIDEN_USERSETTINGS_DB')
_reject_localhost(APPCONFIG_DB_URI, 'UNIDEN_APP_DB')

HPDB_DB_URI = _force_ipv4(_ensure_direct_connection(HPDB_DB_URI))
USERSETTINGS_DB_URI = _force_ipv4(_ensure_direct_connection(USERSETTINGS_DB_URI))
APPCONFIG_DB_URI = _force_ipv4(_ensure_direct_connection(APPCONFIG_DB_URI))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'hpdb': {
        'ENGINE': 'django_mongodb_backend',
        'NAME': 'uniden_hpdb_db',
        'HOST': HPDB_DB_URI,
        **({'USER': HPDB_MONGO_USER} if HPDB_MONGO_USER else {}),
        **({'PASSWORD': HPDB_MONGO_PASSWORD} if HPDB_MONGO_PASSWORD else {}),
    },
    'favorites': {
        'ENGINE': 'django_mongodb_backend',
        'NAME': 'uniden_usersettings_db',
        'HOST': USERSETTINGS_DB_URI,
        **({'USER': USERSETTINGS_MONGO_USER} if USERSETTINGS_MONGO_USER else {}),
        **({'PASSWORD': USERSETTINGS_MONGO_PASSWORD} if USERSETTINGS_MONGO_PASSWORD else {}),
    },
    'appconfig': {
        'ENGINE': 'django_mongodb_backend',
        'NAME': 'uniden_appconfig_db',
        'HOST': APPCONFIG_DB_URI,
        **({'USER': APPCONFIG_MONGO_USER} if APPCONFIG_MONGO_USER else {}),
        **({'PASSWORD': APPCONFIG_MONGO_PASSWORD} if APPCONFIG_MONGO_PASSWORD else {}),
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
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

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

# CORS settings
CORS_ALLOWED_ORIGINS = get_setting(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:9001,http://localhost:8080,http://127.0.0.1:9001',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

CORS_ALLOW_CREDENTIALS = True

# File upload settings
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_NUMBER_FILES = 10000  # Allow up to 10,000 files per upload
UNIDEN_DATA_DIR = get_setting('UNIDEN_DATA_DIR', default=str(BASE_DIR.parent / 'data'))
