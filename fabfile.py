from __future__ import with_statement
from fabric.api import local, settings, abort
from fabric.api import *
from fabric.contrib.console import confirm
from time import sleep

code_dir = '/var/www/yardstick/current'
env.key_filename = "/Users/akfreas/Dropbox/sashimiblade/AppValve-deploy-data/private_keys/Alex-47.pem"
env.host_string = "ubuntu@atyourage.sashimiblade.com"


def deploy():

   print env.key_filename
   with cd(code_dir):
        sudo("GIT_SSH=/home/ubuntu/ssh_git_wrapper.sh git pull origin master")
   restart_server()


def virtualenv(command):
    with cd(env.directory):
        sudo(env.activate + '&&' + command, user=env.deploy_user)


def restart_server():

    stopserver()
    sleep(5)
    startserver()

def startserver():
    sudo("nginx")
    sudo("supervisord")

def stopserver():
    sudo("killall nginx")
    sudo("killall supervisord")

def update_dep():
    with cd(code_dir):
        run("git pull origin master")
        run("source bin/activate && pip install -r requirements.txt")

def update_db():

    with cd(code_dir):
        run("source bin/activate && AtYourAge/manage.py migrate EventApp")


def hello():
        print("Hello world!")
