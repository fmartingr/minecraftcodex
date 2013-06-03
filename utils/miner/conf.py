DEBUG = False

# Save to database?
SAVE = False

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
#   LANGUAGES
###
LANGUAGES_PATH = 'jarfile/lang'
LANGUAGES_MASTER_KEYS = [
    'language.name',
    'language.region',
    'language.code',
]


###
#   ACHIEVEMENTS
###
ACHIEVEMENTS_FILES = []
ACHIEVEMENTS_JAVA_KEYWORDS = ['onARail', 'flyPig']
ACHIEVEMENTS_PATTERN = "new (?P<code>[a-z]{1,2}\((?P<id>[1-9]{1,3})\, \"(?P<name>\w+)\".*\))"


###
#   BLACKLIST
###
CLASS_BLACKLIST = [
    'and', 'abs', 'all', 'any', 'bin', 'chr'
]
