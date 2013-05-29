#!/usr/bin/env python

# General libs
import re
import json
import os
import sys

# Tool libs
from utils import run, sanitize
import conf
from objects import GameBlock


print("=> Phase: blocks")
if conf.SAVE:
    sys.path.append('../../minecraftcodex')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'local_settings'
    from database.models import Block, Texture

###
#   GLOBALS
###
BLOCKS = []

###
#   LOOK FOR CORRECT JAVA FILES
###
print("  => Looking for java files...")
print("     Keywords: %s" % ', '.join(conf.BLOCKS_JAVA_KEYWORDS))
for keyword in conf.BLOCKS_JAVA_KEYWORDS:
    command = run('grep \'%s\' ./classes/*' % keyword)
    lines = []
    [lines.append(x) for x in command]
    lines = ''.join(lines).split('\n')
    for result in lines:
        if result and result is not '':
            java_file = os.path.basename(result.strip().split()[0][:-1])
            if java_file not in conf.BLOCKS_FILES:
                print("     Found: %s" % java_file)
                conf.BLOCKS_FILES.append(java_file)

###
#   GET ITEMS INFO FROM CLASSFILE
###
print("   => Mining blocks...")

# Old items for final count
try:
    OLD_BLOCKS = json.loads(open('blocks.json').read())
except:
    OLD_BLOCKS = {}
    OLD_BLOCKS['list'] = {}

for java_file in conf.BLOCKS_FILES:
    file_handler = open('./classes/%s' % java_file)
    data = file_handler.read().split("\n")

    item_regex = re.compile(conf.BLOCKS_PATTERN)
    class_error_regex = re.compile('name \'(?P<name>\w+)\' is not defined')

    for line in data:
        if '"' in line:  # Reduces iterations
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
                    setattr(sys.modules[__name__], class_name, type(class_name, (GameBlock,), {}))
                    obj = eval(item['code'])

                if conf.DEBUG:
                    print("result object: " + obj.__str__())
                    print('- - - - - -')

                BLOCKS.append(obj)

if conf.SAVE:
    for item in BLOCKS:
        try:
            obj = Block.objects.get(
                internal_name=item.name,
                internal_id=item.id
            )
        except Block.DoesNotExist:
            obj = Block(
                internal_name=item.name,
                internal_id=item.id,
                data_value=item.id
            )
        try:
            texture = Texture.objects.get(name__exact=obj.internal_name)
            obj.main_texture = texture
        except Exception as error:
            print(error)
            pass
        obj.save()

# Print the miner summary and compile the new old data
print('   => Summary')
new_old_data = {}
new_old_data['list'] = []
[new_old_data['list'].append(x.name) for x in BLOCKS]
new_blocks = len(new_old_data['list'])-len(OLD_BLOCKS['list'])
print('   Fetched %d blocks (%d new)' % (len(new_old_data['list']), new_blocks))
if new_blocks > 0:
    print('   Modifications:')
    for item in BLOCKS:
        if item.name not in OLD_BLOCKS['list']:
            print('  + %s' % item.name)

    for item in OLD_BLOCKS['list']:
        if item not in new_old_data['list']:
            print('  - %s' % item)

oldblocks = open('blocks.json', 'w')
oldblocks.write(json.dumps(new_old_data))
