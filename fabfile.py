"""
    fabfile for hitsbook.com
"""

import os.path
from fabric.api import *

env.hosts = ['root@dug0.com:22']
env['dir'] = '/var/webapps/The-Church-of-Horrors'

def deploy():
    with cd(env['dir']):
        run('git pull origin master') # runs the command on the remote environment 

def restart():
    with settings(warn_only=True):
        run('service apache2 reload')

def push():
    local("git push origin master")

def dev():
    env['dir'] = "dev path"

def revert():
    """ Revert git via reset --hard @{1} """
    with cd(env['dir']):
        run('git reset --hard @{1}')
        restart() # restarts server 
        
