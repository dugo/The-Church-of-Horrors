import os
import sys

sys.stdout = sys.stderr

activate = "/var/virtualenvs/thechurch/bin/activate_this.py"
execfile(activate, dict(__file__=activate))

path = '/var/webapps/The-Church-of-Horrors-beta'
if path not in sys.path:
    sys.path.insert(0,path)

path = '/var/webapps/The-Church-of-Horrors-beta/TheChurchofHorrors'
if path not in sys.path:
    sys.path.insert(0,path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'TheChurchofHorrors.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
