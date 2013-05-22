# General libs
from os import listdir
from os.path import isfile, join

# Tool libs
import conf
from objects import GameTexture

print("=> Phase: textures")

TEXTURES = []

for path in conf.TEXTURES_PATHS:
    # GO!
    for f in listdir(path):
        if isfile(join(path, f)):
            TEXTURES.append(GameTexture(f))

print("    Got %d textures" % len(TEXTURES))
