##
#   ITEM
##
class GameItem(object):
    def __init__(self, game_id, *args):
        self.id = int(game_id)

    def __str__(self, *args):
        return "<Item(%d: '%s')>" % (
            self.id,
            self.name
        )

    def method(self, *args):
        if len(args) == 1 and isinstance(args[0], str):
            "Sets the name"
            self.name = args[0]
        return self

    def __getattr__(self, *args):
        return self.method

##
#   BLOCK
##
class GameBlock(object):
    def __init__(self, game_id, *args):
        self.id = int(game_id)

    def __str__(self, *args):
        return "<Block(%d: '%s')>" % (
            self.id,
            self.name
        )

    def method(self, *args):
        if len(args) == 1 and isinstance(args[0], str):
            "Sets the name"
            self.name = args[0]
        return self

    def __getattr__(self, *args):
        return self.method

##
#   TEXTURE
##
class GameTexture(object):
    def __init__(self, name):
        self.name = self.parse_name(name)

    def parse_name(self, name):
        return name.split('.')[0]