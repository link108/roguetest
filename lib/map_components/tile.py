__author__ = 'cmotevasselani'


class Tile:
  # a tile of the map and its properties

  def __init__(self, x, y, blocked, block_sight=None, explored=None):
    self.blocked = blocked
    if explored is None: explored = False
    self.explored = explored
    self.dist_from_player = None
    self.dijkstra_visited = None
    self.x = x
    self.y = y

    # by default, if a tile is blocked, also blocks sight
    if block_sight is None: block_sight = blocked  # must specify block_sight is false to get transparent, impassable tiles
    self.block_sight = block_sight
    self.targeted = False

  def set_blocked(self, value):
    self.blocked = value

  def set_targeted(self, value):
    self.targeted = value

  def set_explored(self, value):
    self.explored = value

  def set_block_sight(self, value):
    self.block_sight = value
