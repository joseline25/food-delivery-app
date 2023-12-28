"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import sys
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_wsgi_application()

# for geoloaction

sys.path.append('C:/OSGeo4W/bin')
os.environ['PATH'] = ';'.join([os.environ['PATH'], 'C:/OSGeo4W/bin'])
