#!/bin/bash

./decompile.sh $1

python textures.py

python items.py

python blocks.py

python languages.py

python achievements.py
