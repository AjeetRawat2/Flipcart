"""
WSGI config for pract project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pract.settings')

application = get_wsgi_application()

# The public Vercel deployment is a portfolio showcase. SQLite is temporary
# there, so initialize its schema for each warm function instance only.
if os.environ.get("VERCEL"):
    call_command("migrate", interactive=False, run_syncdb=True, verbosity=0)
