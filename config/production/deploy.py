# Libs
import sys
import os
from subprocess import call, Popen, PIPE
from shutil import copytree

# Config
APPS_PATH = './app'
CONFIGS_PATH = './config'
APP_DIRECTORY = '%s/minecraftcodex' % APPS_PATH

GIT_REPOSITORY = 'git@bitbucket.org:fmartingr/minecraftcodex.git'
GIT_BRANCH = 'master'
GIT_DOWNLOAD_DIR = './src'
GIT_APP_PATH = 'minecraftcodex'
GIT_PATH_THIS = '%s/config/production/deploy.py' % GIT_DOWNLOAD_DIR

VIRTUALENV_PATH = './virtualenv'

CHECK_SCRIPT_UPDATE = False
THIS_NAME = 'deploy.py'

PYTHON = {
    'py': 'python-2.7',
    'pip': 'pip-2.7',
    'virtualenv': 'virtualenv-2.7'
}

PIP_REQUIREMENTS_FILES = [
    #'%s/config/requirements.pip' % GIT_DOWNLOAD_DIR,
    '%s/config/production/requirements.pip' % GIT_DOWNLOAD_DIR
]

CONFIG_FILES = [
    (
        '%s/config/development/local_settings.py' % GIT_DOWNLOAD_DIR,
        '%s/local_settings.py' % CONFIGS_PATH
    ),
]

FIXTURES = [
    #'%s/config/development/initial_data.json' % GIT_DOWNLOAD_DIR
]

REQUIREMENTS = [
    'git',
]

ENVIRONMENT_VARIABLES = [
    'DATABASE_URL'
]

CONTINUE = True


# Functions
class Colors:
    END = '\033[0m'

    def __init__(self, c='ter,'):
        if c == 'custom':
            self.custom()
        else:
            self.term()

    def custom(self):
        self.WHITE = '\033[89m'
        self.BLACK = '\033[90m'
        self.RED = '\033[91m'
        self.GREEN = '\033[92m'
        self.YELLOW = '\033[93m'
        self.BLUE = '\033[94m'
        self.PURPLE = '\033[95m'
        self.CYAN = '\033[96m'

    def term(self):
        self.WHITE = '\033[29m'
        self.BLACK = '\033[30m'
        self.RED = '\033[31m'
        self.GREEN = '\033[32m'
        self.YELLOW = '\033[33m'
        self.BLUE = '\033[34m'
        self.PURPLE = '\033[35m'
        self.CYAN = '\033[36m'

colors = Colors('custom')


def echo(string, end='\r\n', color=None):
    if color:
        sys.stdout.write("%s%s%s" % (
            color,
            string,
            colors.END
        ))
    else:
        sys.stdout.write(string)
    if end:
        sys.stdout.write("\n")
    sys.stdout.flush()


# Shortcurts
def check_status(status=None, words=['done', 'failed']):
    if status is not None:
        if status == 0:
            echo(words[0], color=colors.GREEN)
        else:
            echo(words[1], color=colors.RED)
            pass
            #exit(-1)


def exists(path):
    return os.path.exists(path)


def title(string):
    print("")
    echo("[==] %s" % string, color=colors.PURPLE)


def info(string):
    echo("[ i] %s" % string, color=colors.BLUE)


def error(string):
    echo("[ E] %s" % string, color=colors.RED)


def success(string):
    echo("[OK] %s" % string, color=colors.GREEN)


def sub(string, end=''):
    echo("     %s " % string, end=end)


# Checking if there's an active virtualenv
if 'VIRTUAL_ENV' in os.environ:
    error('Active virtualenv detected. Deactivate it first.')
    exit(-2)

os.system('clear')
info("Running from %s" % os.getcwd())


# =============== CHECK REQUIREMENTS ===============
title('Checking requirements')
for req in REQUIREMENTS:
    sub('%s:' % req)
    status = call(["which", req], stdout=open(os.devnull, 'wb'))
    check_status(status, words=['present', 'not present'])
    if status != 0:
        CONTINUE = False

# ========== CHECK ENVIRONMENT VARIABLES ==========
title('Checking environment variables')
for env in ENVIRONMENT_VARIABLES:
    sub('%s:' % env)
    if env in os.environ:
        status = 0
    else:
        CONTINUE = False
        status = -1
    check_status(status, words=['present', 'not present'])

# Prequisites check
if not CONTINUE:
    print("")
    error('Prequisites not met. Abort.')
    #error('You should CTRL+C now, errors may occur!')
    exit(1)

# ================== GIT DOWNLOAD ==================
title('Getting last source code')
if not exists(GIT_DOWNLOAD_DIR):
    os.mkdir(GIT_DOWNLOAD_DIR)
    sub('git clone:')
    status = call(['git', 'clone', '-b', GIT_BRANCH, GIT_REPOSITORY, GIT_DOWNLOAD_DIR],
                  stdout=open(os.devnull, 'wb'),
                  stderr=open(os.devnull, 'wb'))
else:
    sub('git pull:')
    status = call(['git', 'pull'], cwd=GIT_DOWNLOAD_DIR,
                  stdout=open(os.devnull, 'wb'),
                  stderr=open(os.devnull, 'wb'))

check_status(status)

# =========== CHECK SCRIPT UPDATE ==================
if CHECK_SCRIPT_UPDATE:
    title('Checking if deploy script is updated on repository')
    actual_size = os.stat('./%s.py' % THIS_NAME).st_size
    repository_size = os.stat(GIT_PATH_THIS).st_size
    if repository_size != actual_size:
        sub('Script is updated.', end='\r\n')

        sub('Deleting old script:')
        status = call(['rm', './%s.py' % THIS_NAME], stdout=open(os.devnull, 'wb'))
        check_status(status)

        sub('Installing new version:')
        status = call(['cp', GIT_PATH_THIS, './%s.py' % THIS_NAME],
                      stdout=open(os.devnull, 'wb'))
        check_status(status)
        info('Restarting execution!')
        os.system('%s ./%s.py' % (PYTHON['py'], THIS_NAME))
        exit(0)
    else:
        sub('Script is up-to-date.', end='\r\n')

# =========== VIRTUALENV =========================
title('Checking and updating virtualenv')
if not exists(VIRTUALENV_PATH):
    sub('Creating virtualenv:')
    status = call([PYTHON['virtualenv'], '-q', '--distribute', VIRTUALENV_PATH],
                  stdout=open(os.devnull, 'wb'))
    check_status(status)
else:
    sub('Virtualenv exists.', end='\r\n')

title('Updating requirements')
for requirements in PIP_REQUIREMENTS_FILES:
    sub('From %s:' % requirements)
    if exists(requirements):
        if os.stat(requirements).st_size > 0:
            status = call(
                'source %s/bin/activate && pip install -r %s' % (
                    VIRTUALENV_PATH,
                    requirements,
                ),
                stdout=open(os.devnull, 'wb'),
                shell=True, executable='/bin/bash'
            )
            check_status(status)
        else:
            echo('empty', color=colors.YELLOW)
    else:
        echo('not exist', color=colors.RED)

# ================== APP INSTALL ==================
title('Installing the app')
sub('Removing old data (if any):')
if exists(APP_DIRECTORY):
    status = call(['rm', '-rf', APP_DIRECTORY],
                  stdout=open(os.devnull, 'wb'))
check_status(status)

if not exists(APPS_PATH):
    call(['mkdir', 'app'])

sub('Copy source to application dir:')
git_path = "%s/%s" % (GIT_DOWNLOAD_DIR, GIT_APP_PATH)
app_path = "%s" % (APP_DIRECTORY)
try:
    copytree(git_path, app_path)
    echo('done', color=colors.GREEN)
except Exception as error:
    echo(error, color=colors.RED)
#status = call(['cp', '-r', git_path, app_path],
#              stdout=open(os.devnull, 'wb'))
#check_status(status)

title('Installing config files')
if not exists(CONFIGS_PATH):
    call(['mkdir', CONFIGS_PATH])
    call(['touch', "%s/__init__.py" % CONFIGS_PATH])

for from_file, to_file in CONFIG_FILES:
    sub('%s:' % os.path.basename(from_file))
    if exists(from_file):
        if os.stat(from_file).st_size > 0:
            status = call(['cp', from_file, to_file],
                          stdout=open(os.devnull, 'wb'))
            check_status(status, words=[os.path.basename(to_file), 'error!'])
        else:
            echo('empty', color=colors.YELLOW)
    else:
        echo('not exists', color=colors.RED)

# ============ DATABASE MIGRATIONS ==============
title('Database migrations')
# Syncdb
sub('Not ready yet!')

print("")
success('Finished!')
