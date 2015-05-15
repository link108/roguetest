
__author__ = 'cmotevasselani'

from lib.random_libs import libtcodpy as libtcod
from lib.constants.map_constants import MapConstants
from lib.utility_functions.object import Object
from lib.utility_functions.util import Util
from lib.map_components.tile import Tile
from lib.map_components.rectangle import Rect
from lib.map_components.item_placer import ItemPlacer
from lib.map_components.monster_placer import MonsterPlacer

DEBUG = False

class MapCreation:
  @staticmethod
  def create_room(game_map, room):
    # go through the tiles in the rectangle and make them passable
    for x in range(room.x1 + 1, room.x2):
      for y in range(room.y1 + 1, room.y2):
        game_map[x][y].set_blocked(False)
        game_map[x][y].set_block_sight(False)

  @staticmethod
  def create_h_tunnel(game_map, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
      game_map[x][y].set_blocked(False)
      game_map[x][y].set_block_sight(False)

  @staticmethod
  def create_v_tunnel(game_map, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
      game_map[x][y].set_blocked(False)
      game_map[x][y].set_block_sight(False)

  @staticmethod
  def create_rect_for_room():
    w = libtcod.random_get_int(0, MapConstants.ROOM_MIN_SIZE, MapConstants.ROOM_MAX_SIZE)
    h = libtcod.random_get_int(0, MapConstants.ROOM_MIN_SIZE, MapConstants.ROOM_MAX_SIZE)
    x = libtcod.random_get_int(0, 0, MapConstants.MAP_WIDTH - w - 1)
    y = libtcod.random_get_int(0, 0, MapConstants.MAP_HEIGHT - h - 1)
    return Rect(x, y, w, h)

  @staticmethod
  def check_for_room_overlap(rooms, new_room):
    failed = False
    for other_room in rooms:
      if new_room.intersect(other_room):
        failed = True
        break
    return failed

  @staticmethod
  def place_objects(state, game_map, room, objects):
    MonsterPlacer.place_monsters(state, game_map, room, objects)
    ItemPlacer.place_items(state, game_map, room, objects)

  @staticmethod
  def make_map(state):
    state.game_map.game_map = [[Tile(True, explored=state.debug)
                               for y in range(MapConstants.MAP_HEIGHT)]
                               for x in range(MapConstants.MAP_WIDTH)]
    rooms = MapCreation.create_rooms(state)
    return rooms

  @staticmethod
  def make_battle_map(state):
    state.game_map.game_map = [[Tile(True, explored=state.debug)
                               for y in range(MapConstants.MAP_HEIGHT)]
                               for x in range(MapConstants.MAP_WIDTH)]
    w = 0
    h = 0
    x = MapConstants.MAP_WIDTH
    y = MapConstants.MAP_HEIGHT
    rooms = [Rect(w, h, x, y)]
    MapCreation.add_room(state, rooms[0], rooms)
    state.player.x, state.player.y = rooms[0].center()
    return rooms

  @staticmethod
  def create_rooms(state):
    rooms = []
    num_rooms = 0
    old_room = None
    for r in range(MapConstants.MAX_ROOMS):
      new_room = MapCreation.create_rect_for_room()
      room_overlaps = MapCreation.check_for_room_overlap(rooms, new_room)
      if not room_overlaps:
        MapCreation.add_room(state, new_room, rooms)
        MapCreation.connect_two_rooms(state.game_map.game_map, old_room, new_room)
        num_rooms += 1
        old_room = new_room
    state.player.x, state.player.y = rooms[0].center()
    return rooms

  @staticmethod
  def place_stairs(state, rooms, old_player_coords):
    down_stairs, up_stairs = MapCreation.generate_stairs(state, rooms)
    MapCreation.create_stairs(state, down_stairs, up_stairs, old_player_coords)

  @staticmethod
  def populate_rooms(state, rooms):
    for room in rooms:
      MapCreation.place_objects(state, state.game_map, room, state.objects_map[state.dungeon_level])

  @staticmethod
  def add_room(state, new_room, rooms):
    MapCreation.create_room(state.game_map.game_map, new_room)
    rooms.append(new_room)

  @staticmethod
  def connect_two_rooms(game_map, old_room, new_room):
    if old_room and new_room:
      choice_points = libtcod.random_get_int(0, 0, 3)
      cx1, cy1 = old_room.center()
      cx2, cy2 = new_room.center()
      rx1, ry1 = old_room.get_random_point()
      rx2, ry2 = new_room.get_random_point()

      if choice_points == 0:
        MapCreation.create_h_tunnel(game_map, cx1, cx2, cy1)
        MapCreation.create_v_tunnel(game_map, cy1, cy2, cx2)
      elif choice_points == 1:
        MapCreation.create_v_tunnel(game_map, cy1, cy2, cx2)
        MapCreation.create_h_tunnel(game_map, cx1, cx2, cy2)
      elif choice_points == 2:
        MapCreation.create_h_tunnel(game_map, rx1, rx2, ry1)
        MapCreation.create_v_tunnel(game_map, ry1, ry2, rx2)
      elif choice_points == 3:
        MapCreation.create_v_tunnel(game_map, ry1, ry2, rx2)
        MapCreation.create_h_tunnel(game_map, rx1, rx2, ry2)

  # TODO Fix this, hacky
  @staticmethod
  def generate_stairs(state, rooms):
    up_stairs_1 = rooms[1].center()
    up_stairs_2 = rooms[2].center()
    player_coords = (state.player.x, state.player.y)
    down_stairs_1 = rooms[3].center()
    down_stairs_2 = rooms[4].center()
    offset_player_coords = (state.player.x - 1, state.player.y - 1)
    down_stairs = [down_stairs_1, down_stairs_2, offset_player_coords]
    up_stairs = [up_stairs_1, up_stairs_2, player_coords]
    return down_stairs, up_stairs

  @staticmethod
  def create_stairs(state, down_stairs_coords, up_stairs_coords, previous_player_coords):
    state.stairs[state.dungeon_level] = {MapConstants.UP_STAIRS_OBJECT: {}, MapConstants.DOWN_STAIRS_OBJECT: {}}
    MapCreation.create_stairs_of_type(state, down_stairs_coords, MapConstants.DOWN_STAIRS_OBJECT)
    MapCreation.create_stairs_of_type(state, up_stairs_coords, MapConstants.UP_STAIRS_OBJECT)
    if state.dungeon_level != 0:
      MapCreation.connect_stairs(state, previous_player_coords)

  @staticmethod
  def create_stairs_of_type(state, stairs_coords, type):
    for stair_coords in stairs_coords:
      stairs = Object(stair_coords[0], stair_coords[1], type, MapConstants.STAIRS_NAME, MapConstants.STAIRS_COLOR,
                      always_visible=True)
      state.objects_map[state.dungeon_level].append(stairs)
      stairs.send_to_back(state.objects_map[state.dungeon_level])
      stairs_id = Util.get_padded_coords(stairs.x, stairs.y)
      state.stairs[state.dungeon_level][type][stairs_id] = None

  @staticmethod
  def connect_stairs(state, previous_player_coords):
    down_stairs_ids = state.stairs[state.dungeon_level - 1][MapConstants.DOWN_STAIRS_OBJECT].keys()
    up_stairs_ids = state.stairs[state.dungeon_level][MapConstants.UP_STAIRS_OBJECT].keys()
    old_down_stair_id = Util.get_padded_coords(previous_player_coords[0], previous_player_coords[1])
    new_up_stair_id = Util.get_padded_coords(state.player.x, state.player.y)
    MapCreation.connect_two_stairs(state, new_up_stair_id, old_down_stair_id)
    down_stairs_ids.remove(old_down_stair_id)
    up_stairs_ids.remove(new_up_stair_id)
    for down_stair_id in down_stairs_ids:
      up_stairs_id = up_stairs_ids.pop()
      MapCreation.connect_two_stairs(state, up_stairs_id, down_stair_id)

  @staticmethod
  def connect_two_stairs(state, new_level_up_stairs_id, prev_level_down_stairs_id):
    state.stairs[state.dungeon_level][MapConstants.UP_STAIRS_OBJECT][new_level_up_stairs_id] = prev_level_down_stairs_id
    state.stairs[state.dungeon_level - 1][MapConstants.DOWN_STAIRS_OBJECT][
      prev_level_down_stairs_id] = new_level_up_stairs_id


