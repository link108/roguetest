__author__ = 'cmotevasselani'

from lib.random_libs import libtcodpy as libtcod
from lib.utility_functions.util import Util
from lib.constants.item_constants import ItemConstants
from lib.constants.equipment_constants import EquipmentConstants


class ItemPlacer:
  @staticmethod
  def place_items(state, game_map, room, objects):
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
    num_items = libtcod.random_get_int(0, 0, max_items)
    for i in range(num_items):
      x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
      y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)
      if not game_map.is_blocked(objects, x, y):
        if libtcod.random_get_int(0, 0, 100) >= 70:
          choice = Util.random_choice(item_chances)
          item_component = state.items.get_data_object(choice)
          item = item_component.get_item(x, y)
        else:
          choice = Util.random_choice(equipment_chances)
          equipment_component = state.equipment.get_data_object(choice)
          item = equipment_component.get_equipment(x, y)
        objects.append(item)
        item.send_to_back(objects)  # items appear below other objects

