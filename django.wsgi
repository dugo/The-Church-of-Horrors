import os
import sys
import site

site.addsitedir('/var/virtualenvs/thechurch/lib/python2.6/site-packages')

path = '/var/webapps/The-Church-of-Horrors'
if path not in sys.path:
    sys.path.insert(0,path)

path = '/var/webapps/The-Church-of-Horrors/TheChurchofHorrors'
if path not in sys.path:
    sys.path.insert(0,path)

path = '/var/virtualenvs/thechurch/lib/python2.6/site-packages'
if path not in sys.path:
    sys.path.insert(0,path)
    
activate = "/var/virtualenvs/thechurch/bin/activate"
execfile(activate, dict(__file__=activate))

os.environ['DJANGO_SETTINGS_MODULE'] = 'TheChurchofHorrors.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
