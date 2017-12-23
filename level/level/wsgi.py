"""
WSGI config for level project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

import sys


path='/var/www/LevelGaming/level/'
sys.path.append(path)
#sys.path.append('/home/danielpeng6/website/LiveMap-Website/django_livemap/livemap')
sys.path.append('/usr/local/lib/python3.6/dist-packages')


from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "level.settings")

application = get_wsgi_application()
