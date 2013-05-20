from __future__ import absolute_import
import os
import sys

# fix sys path so we don't need to setup PYTHONPATH
sys.path.insert(0, os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'minecraftcodex.runtests.settings'

from django.conf import settings
from django.test.utils import get_runner

def usage():
    return """
Usage: python runtests.py [UnitTestClass].[method]

You can pass the Class name of the `UnitTestClass` you want to test.

Append a method name if you only want to test a specific method of that class.
"""


def main():
    TestRunner = get_runner(settings)

    test_runner = TestRunner()
    failures = test_runner.run_tests(['tests'], verbosity=1)

    sys.exit(failures)

if __name__ == '__main__':
    main()
