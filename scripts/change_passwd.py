#!/usr/bin/env python
# coding: utf-8

# generate a random password
from random import choice,seed
import time
import string
import sys,os

seed(time.time())

def GenPasswd():
    chars = string.letters + string.digits
    newpasswd = ''
    for i in range(8):
        newpasswd = newpasswd + choice(chars)
    return newpasswd

activate = "/var/virtualenvs/thechurch/bin/activate_this.py"
execfile(activate, dict(__file__=activate))

# Django environment
PROJECT_PATH = "/var/webapp/SpotMonster"
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","TheChurchofHorrors"))

from django.core.management import setup_environ
sys.path.insert(0,PROJECT_PATH)
import settings
setup_environ(settings)

from django.contrib.auth.models import User

from django.template.loader import render_to_string

for email in sys.argv[1:]:
    
    passwd = GenPasswd()
    u = User.objects.get(username=email.split('@')[0])
    u.save()
    
    # render template
    content = render_to_string('emails/first_email.html', { 'user': u , 'passwd':passwd})
    
    # write email
    open(email,"w").write(content.encode("utf-8"))

