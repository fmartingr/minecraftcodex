#!/usr/bin/env python

# General libs
from os import listdir, environ
from os.path import isfile, join
from sys import path
import json
from PIL import Image

# Tool libs
import conf
from objects import GameTexture

print("=> Phase: textures")

if conf.SAVE:
    path.append('../../minecraftcodex')
    environ['DJANGO_SETTINGS_MODULE'] = 'local_settings'
    from database.models import Texture

TEXTURES = []

# Old textures for final count
try:
    OLD_TEXTURES = json.loads(open('textures.json').read())
except:
    OLD_TEXTURES = {}
    OLD_TEXTURES['list'] = []


for path in conf.TEXTURES_PATHS:
    # GO!
    for f in listdir(path):
        if isfile(join(path, f)):
            if conf.SAVE:
                # Copy original image
                destiny_path = '../../minecraftcodex/database/static/%s' % join(path, f).\
                        replace('jarfile/', '')
                destiny = open(destiny_path, 'w+')
                destiny.write(open(join(path, f)).read())
                destiny.close()
                # making more sizes for the site
                try:
                    modified = Image.open(destiny_path)
                    for multiplier in conf.TEXTURES_EXTRA_SIZES_MULTIPLIER:
                        sizes = (modified.size[0] * multiplier, modified.size[1] * multiplier)
                        modified_path = destiny_path.replace('.png', '_x%d.png' % multiplier)
                        resized = modified.resize(sizes, Image.NEAREST)
                        resized.save(modified_path, 'PNG')
                except IOError:
                    pass

            TEXTURES.append(
                GameTexture(
                    f,
                    path.replace('jarfile/textures/', ''),
                    join(path, f).replace('jarfile/textures/', '')
                )
            )

if conf.SAVE:
    for texture in TEXTURES:
        try:
            item = Texture.objects.get(
                name=texture.name,
                type=texture.type
            )
        except Texture.DoesNotExist:
            item = Texture(
                name=texture.name,
                type=texture.type,
                image=texture.path
            )
            item.save()

print('   => Summary')
new_old_data = {}
new_old_data['list'] = []
[new_old_data['list'].append(x.name) for x in TEXTURES]
new_items = len(new_old_data['list'])-len(OLD_TEXTURES['list'])
print('   Fetched %d textures (%d new)' % (len(TEXTURES), new_items))
if new_items > 0:
    print('   Modifications:')
    for item in TEXTURES:
        if item.name not in OLD_TEXTURES['list']:
            print('  + %s' % item.name)

    for item in OLD_TEXTURES['list']:
        if item not in new_old_data['list']:
            print('  - %s' % item)

olditems = open('textures.json', 'w')
olditems.write(json.dumps(new_old_data))
