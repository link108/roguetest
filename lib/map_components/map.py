
__author__ = 'cmotevasselani'

from lib.map_components.map_creation import MapCreation

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
    if state.dungeon_level >= 1:
      state.player.x, state.player.y = old_player_coords

  def generate_map(self, state, level):
    old_player_coords = (state.player.x, state.player.y)
    rooms = MapCreation.create_map_layout(state, level)
    state.player.x, state.player.y = rooms[0].center()
    MapCreation.place_objects_in_rooms(state, rooms, old_player_coords)

  def set_game_map(self, dungeon_level):
    self.game_map = self.complete_game_map[dungeon_level]

  def get_map(self):
    return self.game_map





