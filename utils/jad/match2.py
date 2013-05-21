#!/usr/bin/env python

import re
import json
import sys
from pprint import pprint

###
#   CONFIGURATION
###

DEBUG = True

ITEMS_FILE = 'wk.java'
BLOCKS_FILE = 'apa.java'

#bL = (new xc(135, 4, 0.6F, apa.ch.cz, apa.aE.cz)).b("carrots");
#bM = (new xc(136, 1, 0.3F, apa.ci.cz, apa.aE.cz)).b("potato");
#bO = (new wf(138, 2, 0.3F, false)).a(mk.u.H, 5, 0, 0.6F).b("potatoPoisonous");
#bQ = (new wf(140, 6, 1.2F, false)).b("carrotGolden").c(xu.l);
#ITEMS_PATTERN = 'new (?P<code>\w{1,2}.*)\;'
ITEMS_PATTERN = "new (?P<code>[a-z]{2}\((?P<id>[1-9]{1,3})[, (?P<hunger>\d+)]?.*\"(?P<name>\w+)\"\))"
BLOCKS_PATTERN = ITEMS_PATTERN

class GameItem(object):
    def __init__(self, game_id, b=None, c=None, d=None, e=None):
        self.game_id = int(game_id)
        pass

    def __str__(self):
        return "<GameItem(%d: '%s')>" % (self.game_id, self.name)

    def b(self, name):
        "Sets the item name."
        self.name = name
        return self

    def d(self, a):
        return self

    def p(self):
        return self

    def j(self):
        return self

    def a(self, a=None, b=None, c=None, d=None, e=None):
        return self

def sanitize(string):
    "Converts parameters and stuff to be correctly evaluated."
    # Remove double parentesis
    sane = string.strip().replace('))', ')')
    # Boolean values
    sane = sane.strip().replace('false', 'False')
    sane = sane.strip().replace('true', 'True')
    # Convert float values to string
    #regex = re.compile('(\d\.\d\w)')
    #sane = regex.sub("'\1'", sane)
    # Convert rest t
    regex = re.compile('([, |\(])([0-9a-zA-Z\.]+)')
    sane = regex.sub(r'\1"\2"', sane)
    return sane

###
#   GLOBALS
###
BLOCKS = []
ITEMS = []

###
#   GET ITEMS INFO FROM CLASSFILE
###
print("=> Mining items")
# Old items for final count
try:
    olditems = open('items.json').read()
    OLD_ITEMS = len(json.loads(olditems))
except:
    OLD_ITEMS = 0

file_handler = open('./classes/%s' % ITEMS_FILE)
data = file_handler.read().split("\n")

item_regex = re.compile(ITEMS_PATTERN)
class_error_regex = re.compile('name \'(?P<name>\w+)\' is not defined')

for line in data:
    if '"' in line:
        t = item_regex.search(line)
        if t:
            item = t.groupdict()
            print("Line: " + item['code'])
            item['code'] = sanitize(item['code'])
            print("Sanitize: " + item['code'])
            try:
                obj = eval(item['code'])
            except NameError as error:
                class_name = class_error_regex.search(error.__str__()).group('name')
                setattr(sys.modules[__name__], class_name, GameItem)
                obj = eval(item['code'])

            print("result object: " + obj.__str__())

            ITEMS.append(obj)
            print('- - - - - -')
print('Fetched %d items (%d new)' % (len(ITEMS), abs(OLD_ITEMS-len(ITEMS))))

#olditems = open('items.json', 'w')
#olditems.write(json.dumps(ITEMS))
