"""
Import all tests.
https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/tests/tests.py
"""
import os

modules = [filename.rsplit('.', 1)[0]
           for filename in os.listdir(os.path.dirname(__file__))
           if filename.endswith('.py') and not filename.startswith('_')]
__test__ = dict()

for module in modules:
    exec("from minecraftcodex.tests.%s import *" % module)
