from lib.random_libs import libtcodpy as libtcod
from lib.constants.map_constants import MapConstants
from lib.utility_functions.util import Util
from lib.utility_functions.object import Object
from lib.constants.item_constants import ItemConstants
from lib.constants.constants import Constants
from lib.items.equipment import Equipment
from lib.items.items import Item


__author__ = 'cmotevasselani'

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
            ItemConstants.SWORD: 50,  # Util.from_dungeon_level(state, [[5, 4]]),
            ItemConstants.SHIELD: 50   # Util.from_dungeon_level(state, [[15, 8]]),
        }
        num_items = libtcod.random_get_int(0, 0, max_items)
        for i in range(num_items):
            x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
            y = libtcod.random_get_int(0, room.y1+1, room.y2-1)
            if not game_map.is_blocked(objects, x, y):
                choice = Util.random_choice(item_chances)
                if choice == ItemConstants.HEALTH_POTION:
                    item_component = state.items.get_item(choice)
                    # item = Object(x, y, item_component.representation, item_component.display_name, item_component.color, item=item_component, always_visible=True)
                    item = item_component.get_item(x, y)
                elif choice == ItemConstants.SCROLL_OF_FIREBALL:
                    item_component = state.items.get_item(choice)
                    item = Object(x, y, item_component.representation, item_component.display_name, item_component.color, item=item_component, always_visible=True)
                elif choice == ItemConstants.SCROLL_OF_CONFUSE:
                    item_component = state.items.get_item(choice)
                    item = Object(x, y, item_component.representation, item_component.display_name, item_component.color, item=item_component, always_visible=True)
                elif choice == ItemConstants.SCROLL_OF_LIGHTNING_BOLT:
                    item_component = state.items.get_item(choice)
                    item = Object(x, y, item_component.representation, item_component.display_name, item_component.color, item=item_component, always_visible=True)

                elif choice == ItemConstants.SWORD:
                    equipment_component = Equipment(Constants.RIGHT_HAND, power_bonus=3)
                    item = Object(x, y, '/', ItemConstants.SWORD, libtcod.red, equipment=equipment_component, always_visible=True)
                elif choice == ItemConstants.SHIELD:
                    equipment_component = Equipment(Constants.LEFT_HAND, defense_bonus=1)
                    item = Object(x, y, '[', ItemConstants.SHIELD, libtcod.darker_orange, equipment=equipment_component, always_visible=True)

                objects.append(item)
                item.send_to_back(objects)  #items appear below other objects

