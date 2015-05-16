__author__ = 'cmotevasselani'

from lib.random_libs import libtcodpy as libtcod
from lib.utility_functions.util import Util
from lib.constants.item_constants import ItemConstants
from lib.constants.equipment_constants import EquipmentConstants


class ItemPlacer:

  @staticmethod
  def place_items_in_room(state, game_map, room, objects):
    items, equipment = ItemPlacer.get_items_to_place(state)
    ItemPlacer.place_items(items, state.items, game_map, room, objects)
    ItemPlacer.place_items(equipment, state.equipment, game_map, room, objects)

  @staticmethod
  def get_items_to_place(state):
    max_items_table = [[3, 0], [5, 3]]
    max_items = Util.from_dungeon_level(state, max_items_table)
    item_chances = {
        ItemConstants.HEALTH_POTION: 35,
        ItemConstants.SCROLL_OF_LIGHTNING_BOLT: Util.from_dungeon_level(state, [[25, 1]]),
        ItemConstants.SCROLL_OF_FIREBALL: Util.from_dungeon_level(state, [[25, 1]]),
        ItemConstants.SCROLL_OF_CONFUSE: Util.from_dungeon_level(state, [[10, 1]]),
    }
    equipment_chances = {
        EquipmentConstants.SWORD: 50,  # Util.from_dungeon_level(state, [[5, 4]]),
        EquipmentConstants.SHIELD: 50  # Util.from_dungeon_level(state, [[15, 8]]),
    }
    num_total_items = libtcod.random_get_int(0, 0, max_items)
    num_items = libtcod.random_get_int(0, 0, num_total_items)
    num_equipments = num_total_items - num_items

    items = [Util.random_choice(item_chances) for i in range(num_items)]
    equipments = [Util.random_choice(equipment_chances) for i in range(num_equipments)]
    return items, equipments

  @staticmethod
  def place_items(objects_to_place, object_data_type, game_map, room, objects):
    for i in range(len(objects_to_place)):
      x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
      y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)
      if not game_map.is_blocked(objects, x, y):
        item_to_place = object_data_type.get_data_object(objects_to_place[i])
        item = item_to_place.create_at_location(x, y)
        objects.append(item)
        item.send_to_back(objects)  # items appear below other objects

