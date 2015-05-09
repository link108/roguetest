
__author__ = 'cmotevasselani'

from lib.map_components.map_creation import MapCreation
from lib.constants.map_constants import MapConstants

class Map:

  def __init__(self, state):
    self.state = state
    self.game_map = None
    self.complete_game_map = {}
    self.stairs_map = {}

  def is_blocked_sight(self, objects, x, y):
    if self.game_map[x][y].block_sight:
      return True
    for object in objects:
      if object.blocks and object.x == x and object.y == y:
        return True
    return False

  def is_blocked(self, objects, x, y):
    if self.game_map[x][y].blocked:
      return True
    for object in objects:
      if object.blocks and object.x == x and object.y == y:
        return True
    return False

  def generate_map(self, state, level):
    old_player_coords = (state.player.x, state.player.y)
    rooms = MapCreation.make_map(state)
    MapCreation.populate_rooms(state, rooms)
    MapCreation.place_stairs(state, rooms, old_player_coords)
    self.complete_game_map[level] = self.game_map

  def set_game_map(self, dungeon_level):
    self.game_map = self.complete_game_map[dungeon_level]

  def get_map(self):
    return self.game_map





