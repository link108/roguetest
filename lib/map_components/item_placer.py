from lib.random_libs import libtcodpy as libtcod
from lib.constants.map_constants import MapConstants
from lib.utility_functions.util import Util
from lib.utility_functions.object import Object
from lib.constants.item_constants import ItemConstants
from lib.constants.constants import Constants
from lib.items.equipment import Equipment


__author__ = 'cmotevasselani'

class ItemPlacer:


    @staticmethod
    def place_items(state, game_map, room, objects):
        max_items_table = [[3, 0], [5, 3]]
        max_items = Util.from_dungeon_level(state, max_items_table)
        item_chances = {
            MapConstants.HEALTH_POTION: 35,
            MapConstants.SCROLL_OF_LIGHTNING_BOLT: Util.from_dungeon_level(state, [[25, 1]]),
            MapConstants.SCROLL_OF_FIREBALL: Util.from_dungeon_level(state, [[25, 1]]),
            MapConstants.SCROLL_OF_CONFUSE: Util.from_dungeon_level(state, [[10, 1]]),
            MapConstants.SWORD: 50,  # Util.from_dungeon_level(state, [[5, 4]]),
            MapConstants.SHIELD: 50   # Util.from_dungeon_level(state, [[15, 8]]),
        }
        #choose random number of items
        num_items = libtcod.random_get_int(0, 0, max_items)
        for i in range(num_items):
            #choose random spot for this item
            x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
            y = libtcod.random_get_int(0, room.y1+1, room.y2-1)
            #only place it if the tile is not blocked
            if not game_map.is_blocked(objects, x, y):
                choice = Util.random_choice(item_chances)
                if choice == MapConstants.HEALTH_POTION:
                    #create a healing potion
                    item_component = state.items.get_item(ItemConstants.HEALTH_POTION)
                    item = Object(x, y, '!', MapConstants.HEALTH_POTION, libtcod.violet, item=item_component, always_visible=True)
                elif choice == MapConstants.SCROLL_OF_FIREBALL:
                    item_component = state.items.get_item(ItemConstants.CAST_FIREBALL)
                    item = Object(x, y, '#', MapConstants.SCROLL_OF_FIREBALL, libtcod.light_yellow, item=item_component, always_visible=True)
                elif choice == MapConstants.SCROLL_OF_CONFUSE:
                    item_component = state.items.get_item(ItemConstants.CAST_CONFUSE)
                    item = Object(x, y, '#', MapConstants.SCROLL_OF_CONFUSE, libtcod.light_yellow, item=item_component, always_visible=True)
                elif choice == MapConstants.SCROLL_OF_LIGHTNING_BOLT:
                    item_component = state.items.get_item(ItemConstants.CAST_LIGHTNING)
                    item = Object(x, y, '#', MapConstants.SCROLL_OF_LIGHTNING_BOLT, libtcod.light_yellow, item=item_component, always_visible=True)
                elif choice == MapConstants.SWORD:
                    equipment_component = Equipment(Constants.RIGHT_HAND, power_bonus=3)
                    item = Object(x, y, '/', MapConstants.SWORD, libtcod.red, equipment=equipment_component, always_visible=True)
                elif choice == MapConstants.SHIELD:
                    equipment_component = Equipment(Constants.LEFT_HAND, defense_bonus=1)
                    item = Object(x, y, '[', MapConstants.SHIELD, libtcod.darker_orange, equipment=equipment_component, always_visible=True)

                objects.append(item)
                item.send_to_back(objects)  #items appear below other objects

