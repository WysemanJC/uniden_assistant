"""
WSGI config for uniden_assistant project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniden_assistant.settings')

application = get_wsgi_application()
