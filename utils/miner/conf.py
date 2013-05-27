DEBUG = False

SAVE = True

###
#   TEXTURES
###
TEXTURES_PATHS = ['jarfile/textures/blocks', 'jarfile/textures/items']
TEXTURES_EXTRA_SIZES_MULTIPLIER = [2, 4, 6, 8]

###
#   ITEMS
###

ITEMS_FILES = []
ITEMS_JAVA_KEYWORDS = ['flintAndSteel', 'axeStone', 'swordDiamond']
ITEMS_PATTERN = "new (?P<code>[a-z]{2}\((?P<id>[1-9]{1,3}).*\"(?P<name>\w+)\"\))"

###
#   BLOCKS
###

BLOCKS_FILES = []
BLOCKS_JAVA_KEYWORDS = ['stonebrick']
BLOCKS_PATTERN = "new (?P<code>[a-z]{1,3}\((?P<id>[1-9]{1,3}).*\"(?P<name>\w+)\"\))"

###
#   BLACKLIST
###

CLASS_BLACKLIST = [
    'and', 'abs', 'all', 'any', 'bin', 'chr'
]
