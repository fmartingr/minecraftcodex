#!/usr/bin/env python

# General libs
import re
import json
import os
import sys

# Tool libs
from utils import run, sanitize
import conf
from objects import GameItem


print("=> Phase: items")


###
#   GLOBALS
###
ITEMS = []

###
#   LOOK FOR CORRECT JAVA FILES
###
print("   => Looking for java files...")
print("     Keywords: %s" % ', '.join(conf.ITEMS_JAVA_KEYWORDS))
for keyword in conf.ITEMS_JAVA_KEYWORDS:
    cmd = run('grep \'%s\' ./classes/*' % keyword)
    for result in cmd:
        if result and result is not '':
            java_file = os.path.basename(result.strip().split()[0][:-1])
            if java_file not in conf.ITEMS_FILES:
                print("     Found: %s" % java_file)
                conf.ITEMS_FILES.append(java_file)

###
#   GET ITEMS INFO FROM CLASSFILE
###
print("  => Mining items...")

# Old items for final count
try:
    OLD_ITEMS = json.loads(open('items.json').read())
except:
    OLD_ITEMS = {}
    OLD_ITEMS['list'] = []

for java_file in conf.ITEMS_FILES:
    file_handler = open('./classes/%s' % java_file)
    data = file_handler.read().split("\n")

    item_regex = re.compile(conf.ITEMS_PATTERN)
    class_error_regex = re.compile('name \'(?P<name>\w+)\' is not defined')

    for line in data:
        if '"' in line:
            t = item_regex.search(line)
            if t:
                item = t.groupdict()
                if conf.DEBUG:
                    print("Line: " + item['code'])

                item['code'] = sanitize(item['code'])

                if conf.DEBUG:
                    print("Sanitize: " + item['code'])

                try:
                    obj = eval(item['code'])
                except NameError as error:
                    # Create class for the given classname
                    class_name = class_error_regex.search(error.__str__()).group('name')
                    if conf.DEBUG:
                        print("Classname: %s" % class_name)
                    setattr(sys.modules[__name__], class_name, type(class_name, (GameItem,), {}))
                    obj = eval(item['code'])
                #if obj.name == 'appleGold':
                if conf.DEBUG:
                    print("result object: " + obj.__str__())
                    print('- - - - - -')

                ITEMS.append(obj)

# Print the miner summary and compile the new old data
print('   => Summary')
new_old_data = {}
new_old_data['list'] = []
[new_old_data['list'].append(x.name) for x in ITEMS]
new_items = len(new_old_data['list'])-len(OLD_ITEMS['list'])
print('   Fetched %d items (%d new)' % (len(ITEMS), new_items))
print('   Modifications:')
for item in ITEMS:
    if item.name not in OLD_ITEMS['list']:
        print('  + %s' % item.name)

for item in OLD_ITEMS['list']:
    if item not in new_old_data['list']:
        print('  - %s' % item)

olditems = open('items.json', 'w')
olditems.write(json.dumps(new_old_data))
