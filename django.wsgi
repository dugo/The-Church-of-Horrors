import os
import sys
import site

site.addsitedir('/var/virtualenvs/thechurch/lib/python2.6/site-packages')

path = '/var/webapp'
if path not in sys.path:
    sys.path.insert(0,path)

path = '/var/webapp/SpotMonster'
if path not in sys.path:
    sys.path.insert(0,path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'SpotMonster.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
