
__author__ = 'cmotevasselani'

from lib.random_libs import libtcodpy as libtcod
from lib.constants.constants import Constants
from lib.utility_functions.util import Util
from lib.utility_functions.object import Object

# Must include all item modules here
from item_functions.potion_functions import PotionFunctions
from item_functions.scroll_functions import ScrollFunctions

class Item:

    def __init__(self, name=None, item_string=None):
        if name and item_string:
            self.name = name
            self.display_name = self.name.replace('_', ' ')
            item_info = item_string.strip().split('_XXX_')
            self.item_class = item_info[0]
            self.item_function = item_info[1]
            self.representation = item_info[2]
            self.color = getattr(libtcod, item_info[3])
            self.always_visible = bool(item_info[4])

    def pick_up(self, state):
        if len(state.player_inventory.inventory) >= 26:
            state.inventory.status_panel.message('Your inventory is full, cannot pick up ' + self.owner.name + '.', libtcod.red)
        else:
            state.player_inventory.inventory.append(self.owner)
            state.objects.remove(self.owner)
            state.status_panel.message('You picked up a ' + self.owner.name + '!', libtcod.green)
            equipment = self.owner.equipment
            if equipment and Util.get_equipped_in_slot(state, equipment.slot) is None:
                equipment.equip(state)

    def use(self, state):
        #call use_function if defined
        if self.owner.equipment:
            self.owner.equipment.toggle_equipment(state)
            return
        if self.item_class and self.item_function:
            use_function = getattr(eval(self.item_class), self.item_function)
        if use_function is None:
            state.status_panel.message('The ' + self.owner.name + ' cannot be used.')
        else:
            if use_function(state) != Constants.CANCELLED:
                state.player_inventory.inventory.remove(self.owner)    #destroy after use, unless cancelled

    def drop(self, state):
        state.objects.append(self.owner)
        state.player_inventory.inventory.remove(self.owner)
        self.owner.x = state.player.x
        self.owner.y = state.player.y
        state.status_panel.message('You drop a ' + self.owner.name + '.', libtcod.turquoise)

    def get_item(self, x, y):
        return Object(x, y,
                      self.representation,
                      self.display_name,
                      self.color,
                      item=self,
                      always_visible=self.always_visible)
