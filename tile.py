__author__ = 'cmotevasselani'





class Tile:
    #a tile of the map and its properties

    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        self.explored = False

        #by default, if a tile is blocked, also blocks sight
        if block_sight is None: block_sight = blocked           #must specify block_sight is false to get transparent, impassable tiles
        self.block_sight = block_sight

    def set_blocked(self, value):
        self.blocked = value

    def set_explored(self, value):
        self.explored = value

    def set_block_sight(self, value):
        self.block_sight = value
