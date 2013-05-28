#!/usr/bin/env python

# General libs
import re
import json
import os
import sys

# Tool libs
from utils import run, sanitize
import conf
from objects import GameLanguage


print("=> Phase: languages")
if conf.SAVE:
    sys.path.append('../../minecraftcodex')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'local_settings'
    from database.models import Language, LanguageString

###
#   GLOBALS
###
STRINGS = []
LANGUAGES = []
LANGUAGES_STR = []

###
#   LOOK FOR CORRECT JAVA FILES
###
print("   => Looking for languages files...")
directory_list = os.listdir(conf.LANGUAGES_PATH)
print("      Found %d file(s)." % len(directory_list))

###
#   GET LANGUAGES
###
try:
    OLD_STRINGS = json.loads(open('strings.json').read())
except:
    OLD_STRINGS = []
try:
    OLD_LANGUAGES = json.loads(open('languages.json').read())
except:
    OLD_LANGUAGES = []

print("   => Mining languages...")
for item in directory_list:
    if '.lang' in item:
        if conf.DEBUG:
            print("      Now %s " % item)

        language = open('%s/%s' % (conf.LANGUAGES_PATH, item))
        language_obj = GameLanguage()
        for line in language.readlines():
            line = line.strip()
            if line and 'X-Generator' not in line:
                key, value = line.split('=', 1)
                if key in conf.LANGUAGES_MASTER_KEYS:
                    # Language object
                    setattr(language_obj, key.split('.')[1], value)
                else:
                    # Language String object
                    language_obj.add_string(key, value)

                    # Store for comparision
                    if language_obj.code == 'en_US':
                        if key not in STRINGS:
                            STRINGS.append(key)
        LANGUAGES.append(language_obj)

if conf.SAVE:
    for item in LANGUAGES:
        try:
            obj = Language.objects.get(
                name=item.name,
                region=item.region,
                code=item.code
            )
        except Language.DoesNotExist:
            obj = Language(
                name=item.name,
                region=item.region,
                code=item.code
            )
            obj.save()
        for key in item.strings.keys():
            value = item.strings[key]
            try:
                string_obj = LanguageString.objects.get(
                    language=obj,
                    key=key
                )
                if string_obj.value != value:
                    string_obj.value = value
                    string_obj.save()
            except LanguageString.DoesNotExist:
                string_obj = LanguageString(
                    language=obj,
                    key=key,
                    value=value
                )
                string_obj.save()



print("   => Summary")

# LANGUAGES
[LANGUAGES_STR.append(x.name) for x in LANGUAGES]
new_languages = len(LANGUAGES_STR) - len(OLD_LANGUAGES)
print("      Found %d languages (%d new)." % (len(LANGUAGES_STR), new_languages))
if len(LANGUAGES_STR) != len(OLD_LANGUAGES):
    print("      Comparision:")

    for string in LANGUAGES_STR:
        if string not in OLD_LANGUAGES:
            print("       + %s" % string)

    for string in OLD_LANGUAGES:
        if string not in LANGUAGES_STR:
            print("       - %s" % string)

olditems = open('languages.json', 'w')
olditems.write(json.dumps(LANGUAGES_STR))
olditems.close()

# STRINGS
new_strings = len(STRINGS) - len(OLD_STRINGS)
print("      Found %d strings (%d new) -based on en_US-." % (len(STRINGS), new_strings))
if len(STRINGS) != len(OLD_STRINGS):
    print("      Comparision:")

    for string in STRINGS:
        if string not in OLD_STRINGS:
            print("       + %s" % string)

    for string in OLD_STRINGS:
        if string not in STRINGS:
            print("       - %s" % string)
            
olditems = open('strings.json', 'w')
olditems.write(json.dumps(STRINGS))
olditems.close()
