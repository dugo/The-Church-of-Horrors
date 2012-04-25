#!/usr/bin/env python
# coding: utf-8


# generate a random password
from random import choice,seed
import time
import string
import sys,os

if len(sys.argv)<>3:
    print "Usage: %s <email> <fullname>"
    sys.exit()

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
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","TheChurchofHorrors"))

from django.core.management import setup_environ
sys.path.insert(0,PROJECT_PATH)
import settings
settings.DEBUG=True
setup_environ(settings)

from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User,Group
from django.core.mail import send_mail

# data
passwd = GenPasswd()
username = sys.argv[1].split("@")[0]
email = sys.argv[1]
name = sys.argv[2].title()
group = Group.objects.get(name="Redactor")

# create user
u = User(username=username,email=email,first_name=name)

# set staff
u.staff = True
u.is_superuser = False

# set password
u.set_passwd(passwd)

u.save()

# set group
u.groups = [group]

u.save()

# send email

# render template
email = render_to_string('emails/first_email.html', { 'user': u , 'passwd':passwd})

# send email
send_mail('Bienvenido a TheChurchofHorrors', email, u'Rubén Dugo <rdugo@thechurchofhorrors.com>', [emails[i]], fail_silently=False)


