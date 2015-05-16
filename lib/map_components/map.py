
__author__ = 'cmotevasselani'

from lib.map_components.map_creation import MapCreation
from lib.constants.map_constants import MapConstants

class Map:

  def __init__(self):
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

  def generate_battle_map(self, state):
    old_player_coords = (state.player.x, state.player.y)
    rooms = MapCreation.make_battle_map(state)
    MapCreation.populate_rooms(state, rooms)
    self.complete_game_map[0] = self.game_map

  def generate_map(self, state, level):
    old_player_coords = (state.player.x, state.player.y)
    rooms = self.create_map_layout(state, level)
    state.player.x, state.player.y = rooms[0].center()
    self.place_objects_in_rooms(state, rooms, old_player_coords)

  def create_map_layout(self, state, level):
    rooms = MapCreation.make_map(state)
    self.complete_game_map[level] = self.game_map
    return rooms

  def place_objects_in_rooms(self, state, rooms, old_player_coords):
    MapCreation.populate_rooms(state, rooms)
    MapCreation.place_stairs(state, rooms, old_player_coords)

  def set_game_map(self, dungeon_level):
    self.game_map = self.complete_game_map[dungeon_level]

  def get_map(self):
    return self.game_map





