# Libs
import sys
import os
from subprocess import call, Popen, PIPE
from shutil import copytree

# Config
APP_DIRECTORY = './app'

GIT_REPOSITORY = 'git@bitbucket.org:fmartingr/minecraftcodex.git'
GIT_DOWNLOAD_DIR = './src'
GIT_APP_PATH = 'minecraftcodex'
GIT_PATH_THIS = '%s/config/production/deploy.py' % GIT_DOWNLOAD_DIR

VIRTUALENV_PATH = './virtualenv'

CHECK_SCRIPT_UPDATE = False

PYTHON = {
    'py': 'python-2.7',
    'pip': 'pip-2.7',
    'virtualenv': 'virtualenv-2.7'
}

PIP_REQUIREMENTS_FILES = [
    '%s/config/production/requirements.pip' % GIT_DOWNLOAD_DIR
]

CONFIG_FILES = [
    (
        '%s/config/production/local_settings.py' % GIT_DOWNLOAD_DIR,
        '%s/herobrine/local_settings.py' % APP_DIRECTORY
    ),
]

FIXTURES = [
    #'%s/config/production/initial_data.json' % GIT_DOWNLOAD_DIR
]

REQUIREMENTS = [
    'git', 'coffee', 'lessc', 'uglifyjs'
]

# Paths relatives to APP DIR
PREPROCESSORS = {
    'coffee': {
        'items': [
            #('shoes/static/coffee/usc.coffee', 'shoes/static/js/usc.big.js'),
        ],
        'params': ''
    },
    'less': {
        'items': [
            #('shoes/static/less/style.less', 'shoes/static/css/style.css'),
        ],
        'params': '-s -x'
    },
    'uglify': {
        'items': [
            #('shoes/static/js/usc.big.js', 'shoes/static/js/usc.js'),
        ],
        'params': '-c warnings=false'
    }
}

ENVIRONMENT_VARIABLES = [
    'DATABASE_HOST',
    'DATABASE_USER',
    'DATABASE_PASS',
    'DATABASE_PORT',
    'DATABASE_NAME'
]

SERVER_PORT = 8001
RUNSERVER_PARAMS = "0.0.0.0:%d" % SERVER_PORT

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
    exit(-1)

# ================== GIT DOWNLOAD ==================
title('Getting last source code')
"""
if not exists(GIT_DOWNLOAD_DIR):
    os.mkdir(GIT_DOWNLOAD_DIR)
    sub('git clone:')
    status = call(['git', 'clone', GIT_REPOSITORY, GIT_DOWNLOAD_DIR],
                  stdout=open(os.devnull, 'wb'),
                  stderr=open(os.devnull, 'wb'))
else:
    sub('git pull:')
    status = call(['git', 'pull'], cwd=GIT_DOWNLOAD_DIR,
                  stdout=open(os.devnull, 'wb'),
                  stderr=open(os.devnull, 'wb'))

check_status(status)
"""
# =========== CHECK SCRIPT UPDATE ==================
title('Checking if deploy script is updated on repository')
actual_size = os.stat('./deploy.py').st_size
repository_size = os.stat(GIT_PATH_THIS).st_size
if repository_size != actual_size and CHECK_SCRIPT_UPDATE:
    sub('Script is updated.', end='\r\n')

    sub('Deleting old script:')
    status = call(['rm', './deploy.py'], stdout=open(os.devnull, 'wb'))
    check_status(status)

    sub('Installing new version:')
    status = call(['cp', GIT_PATH_THIS, './deploy.py'],
                  stdout=open(os.devnull, 'wb'))
    check_status(status)
    info('Restarting execution!')
    os.system('%s ./deploy.py' % PYTHON['py'])
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

#call(['mkdir', APP_DIRECTORY])
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
for from_file, to_file in CONFIG_FILES:
    sub('%s:' % os.path.basename(from_file))
    if exists(from_file):
        if os.stat(from_file).st_size > 0:
            status = call(['cp', from_file, to_file],
                          stdout=open(os.devnull, 'wb'))
            check_status(status)
        else:
            echo('empty', color=colors.YELLOW)
    else:
        echo('not exists', color=colors.RED)

# ============ DATABASE MIGRATIONS ==============
title('Database migrations')
# Syncdb
sub('django syncdb:')
status = call(
    'source %s/bin/activate && python %s/manage.py syncdb --noinput' % (
        VIRTUALENV_PATH,
        APP_DIRECTORY
    ),
    stdout=open(os.devnull, 'wb'),
    shell=True, executable='/bin/bash'
)
check_status(status)
if FIXTURES:
    # Loading fixtures
    for fixture in FIXTURES:
        sub('[fixture] %s:' % fixture)
        status = call(
            'source %s/bin/activate && python %s/manage.py loaddata %s' % (
                VIRTUALENV_PATH,
                APP_DIRECTORY,
                fixture
            ),
            stdout=open(os.devnull, 'wb'),
            shell=True, executable='/bin/bash'
        )
        check_status(status, words=['installed', 'not installed'])

# South migrate
sub('south migrate:')
status = call(
    'source %s/bin/activate && python %s/manage.py migrate' % (
        VIRTUALENV_PATH,
        APP_DIRECTORY
    ),
    stdout=open(os.devnull, 'wb'),
    shell=True, executable='/bin/bash'
)
check_status(status)

# ================= COMPILERS ===================
if PREPROCESSORS['coffee']['items']:
    title('Coffeescript compiling')
    for coffee in PREPROCESSORS['coffee']['items']:
        sub("%s:" % coffee[0])
        path = "%s/%s" % (APP_DIRECTORY, coffee[0])
        path_to = "%s/%s" % (APP_DIRECTORY, coffee[1])
        params = ['coffee', '-p', path, '>', path_to]
        status = call(" ".join(params),
                      stdout=open(os.devnull, 'wb'),
                      shell=True)
        check_status(status, words=[os.path.basename(path_to), 'failed'])

if PREPROCESSORS['uglify']['items']:
    title('Javascript compressing')
    sub('Original files are removed.', end='\r\n')
    for javascript in PREPROCESSORS['uglify']['items']:
        sub("+ %s:" % javascript[0])
        path = "%s/%s" % (APP_DIRECTORY, javascript[0])
        path_to = "%s/%s" % (APP_DIRECTORY, javascript[1])
        params = ['uglifyjs', path, PREPROCESSORS['uglify']['params'], '>', path_to]
        status = call(" ".join(params),
                      stdout=open(os.devnull, 'wb'),
                      stderr=open(os.devnull, 'wb'),
                      shell=True)
        check_status(status, words=[os.path.basename(path_to), 'failed'])
        sub('- Deleting %s:' % path)
        status = call(['rm', path],
                      stdout=open(os.devnull, 'wb'),
                      stderr=open(os.devnull, 'wb'))
        check_status(status)

if PREPROCESSORS['less']['items']:
    title('LESS compiling and CSS compressing')
    for item in PREPROCESSORS['less']['items']:
        sub("%s:" % item[0])
        path = "%s/%s" % (APP_DIRECTORY, item[0])
        path_to = "%s/%s" % (APP_DIRECTORY, item[1])
        params = ['lessc', PREPROCESSORS['less']['params'], path, '>', path_to]
        status = call(" ".join(params),
                      stdout=open(os.devnull, 'wb'),
                      shell=True)
        check_status(status, words=[os.path.basename(path_to), 'failed'])

title('Collecting all staticfiles')
sub('manage.py collectstatic')
status = call(
    'source %s/bin/activate && python %s/manage.py collectstatic --noinput' % (
        VIRTUALENV_PATH,
        APP_DIRECTORY
    ),
    stdout=open(os.devnull, 'wb'),
    shell=True, executable='/bin/bash'
)
check_status(status)
# ================ SERVER =======================


print("")
success('Finished!')
