from __future__ import with_statement
from fabric.api import local, settings, abort
from fabric.api import *
from fabric.contrib.console import confirm
from time import sleep

env.hosts = ['ubuntu@23.21.141.254']
code_dir = '/var/www/AtYourAge-env/AtYourAge'

def deploy():
    with cd(code_dir):
        sudo("git pull origin master")
    restart_server()


def virtualenv(command):
    with cd(env.directory):
        sudo(env.activate + '&&' + command, user=env.deploy_user)


def restart_server():

    stopserver()
    sleep(10)
    startserver()

def startserver():
    sudo("nginx")

def stopserver():
    sudo("killall nginx")

def update_dep():
    with cd(code_dir):
        run("git pull origin master")
        run("source bin/activate && pip install -r requirements.txt")

def update_db():

    with cd(code_dir):
        run("source bin/activate && AtYourAge/manage.py migrate MainSite")


def hello():
        print("Hello world!")
