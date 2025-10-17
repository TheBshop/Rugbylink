"""
WSGI config for web_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from django.core.wsgi import get_wsgi_application

# Use production settings if DJANGO_SETTINGS_MODULE is not set
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_django.settings_production")

application = get_wsgi_application()
