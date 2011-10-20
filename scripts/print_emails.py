#!/usr/bin/env python
# coding: utf-8
import sys,os

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


for i in range(len(emails)):
    
    print "%s\t\t%s" % (emails[i], org_email[i],)

