##
# This fabric script only add automation to tasks for
# local development, is not intended to be used for
# deploys or stuff.
##

# IMPORTS
from fabric.api import local, env, prefix, execute
from fabric.context_managers import settings, hide
from os.path import exists
from os import environ, stat, getcwd
from fabric.colors import yellow, red, green
from subprocess import PIPE, Popen
import sys

# Fabric env
env.hosts = ['localhost']
env.activate = 'source virtualenv/bin/activate'
env.python = None

# Development data
env.development_ddbb = 'dev.sqlite3'

# Configuration
#python_version = "3.3.1"
python_version = "2.7.5"


# Functions
def echo(string, end='\r\n'):
    sys.stdout.write(string)
    if end:
        sys.stdout.write("\n")
    sys.stdout.flush()


def active_virtualenv():
    result = 'VIRTUAL_ENV' in environ
    if result:
        print red("Active virtualenv detected! You must deactivate it first.")
        exit(-1)
    return result


def python():
    if env.python is None:
        print(yellow('Looking for python %s ...' % python_version))

        # System python
        echo(yellow('- System python: '), end='')
        active = Popen('python --version',
                       stdout=PIPE,
                       stderr=PIPE,
                       shell=True)
        version = active.communicate()[1].split()[1]
        if version == python_version:
            print(green('found!'))
            env.python = 'python'
            return(env.python)
        else:
            print(red(version))

        # Alternate install
        echo(yellow('- Alternate install: '), end='')
        active = Popen('python3 --version',
                       stdout=PIPE,
                       stderr=PIPE,
                       shell=True)
        version = active.communicate()[1].split()[1]
        if version == python_version:
            print(green('found!'))
            env.python = 'python3'
            return(env.python)
        else:
            if active.returncode == 0:
                print(red(version))
            else:
                print(red('not found'))

        # PythonZ
        echo(yellow('- PythonZ: '), end='')
        active = Popen('$HOME/.pythonz/pythons/CPython-3.3.1/bin/python3 --version',
                       stdout=PIPE,
                       stderr=PIPE,
                       shell=True)
        output = active.communicate()
        version = output[1].split()[1]
        if version == python_version:
            print(green('found!'))
            env.python = "~/.pythonz/pythons/CPython-3.3.1/bin/python3"
            return(env.python)
        else:
            if active.returncode == 0:
                print(red(version))
            else:
                print(red('not found'))

        # Anything found? D:
        print(red('Python %s was not found!' % python_version))
        exit(-1)
    else:
        return env.python


# Virtualenv
def create_virtualenv():
    if not exists('./virtualenv'):
        print(yellow('Making virtualenv'))
        local("virtualenv -q --distribute -p %s ./virtualenv" % python())
    else:
        print(green('Virtualenv already exists.'))


# Requirements
def install_requirements():
    if not active_virtualenv():
        with prefix(env.activate):
            if stat('./config/development/requirements.pip').st_size > 0:
                print(yellow('Installing development requirements'))
                local('pip install -q -r ./config/development/requirements.pip')


def install(package):
    "Install packages on the environment using fab install:<package name>"
    if not active_virtualenv():
        with prefix(env.activate):
            local('pip install ' + package)


def requirements(environ='global'):
    if not active_virtualenv():
        with prefix(env.activate):
            local('pip freeze')


def syncdb():
    if not active_virtualenv():
        with prefix(env.activate):
            local('python minecraftcodex/manage.py syncdb --noinput')
            local('python minecraftcodex/manage.py loaddata ./config/development/admin.json')
            local('python minecraftcodex/manage.py migrate')


def schemamigration(app, flag='--auto'):
    if not active_virtualenv():
        with prefix(env.activate):
            local('python minecraftcodex/manage.py schemamigration %s %s' % (app, flag))


# Easy-mode
def prepare():
    execute(create_virtualenv)
    execute(install_requirements)


def p():
    execute(prepare)


def run():
    if not active_virtualenv():
        with prefix(env.activate):
            path = getcwd()
            with settings(hide('warnings', 'running'),
                          warn_only=True):
                local('ln -s %s/config/development/local_settings.py %s/minecraftcodex/herobrine/local_settings.py' % (path, path))
                local('python minecraftcodex/manage.py runserver')
            local('rm ./minecraftcodex/herobrine/local_settings.py')

def test():
    if not active_virtualenv():
        with prefix(env.activate):
            local('python -m unittest discover')
            with settings(hide('warnings', 'running', 'stdout', 'stderr'),
                          warn_only=True):
                local('find . -type d -name __pycache__ -exec rm -rf {} \;',
                      capture=True)


def tox():
    local('tox')
    with settings(hide('warnings', 'running', 'stdout', 'stderr'),
                  warn_only=True):
        local('find . -type d -name __pycache__ -exec rm -rf {} \;',
              capture=True)
