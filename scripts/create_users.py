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

from django.conf import settings
from django.template.loader import render_to_string
from modules.userprofile.models import UserProfile
from django.contrib.auth.models import User,Group
from django.core.mail import send_mail

emails = []
nombres = []
org_email = []

i=0
for l in open(sys.argv[1]).readlines():
    if i%3==0:
        nombres.append(l.strip(" \n").lower())
    elif i%3==1:
        emails.append(l.strip(" \n").lower())
    else:
        org_email.append(l.strip(" \n").lower())
    
    i+=1

group = Group.objects.get(name="Redactor")

for i in range(len(emails)):
    
    passwd = GenPasswd()
    
    u = User(email=emails[i],username=emails[i].split('@')[0],first_name=nombres[i].title())
    u.set_password(passwd)
    u.is_staff=True
    u.is_superuser = False
    u.save()
    u.groups.add(group)
    u.save()
    
    # render template
    email = render_to_string('emails/first_email.html', { 'user': u , 'passwd':passwd})
    
    # send email
    send_mail('Bienvenido a TheChurchofHorrors', email, u'Rubén Dugo <rdugo@thechurchofhorrors.com>', [emails[i]], fail_silently=False)
    time.sleep(5)

