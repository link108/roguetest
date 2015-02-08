from lib.random_libs import libtcodpy as libtcod

__author__ = 'cmotevasselani'

from lib.constants.constants import Constants
from lib.utility_functions.util import Util


class Item:

    def __init__(self, use_function=None):
        self.use_function = use_function

    # an item that can be picked up and used.
    def pick_up(self, state):
        #add to the player's inventory and remove from the map
        if len(state.player_inventory.inventory) >= 26:
            state.inventory.status_panel.message('Your inventory is full, cannot pick up ' + self.owner.name + '.', libtcod.red)
        else:
            state.player_inventory.inventory.append(self.owner)
            state.objects.remove(self.owner)
            state.status_panel.message('You picked up a ' + self.owner.name + '!', libtcod.green)
            equipment = self.owner.equipment
            if equipment and Util.get_equipped_in_slot(state, equipment.slot) is None:
                equipment.equip()

    def use(self, state):
        #call use_function if defined
        if self.owner.equipment:
            self.owner.equipment.toggle_equipment(state)
            return
        if self.use_function is None:
            state.status_panel.message('The ' + self.owner.name + ' cannot be used.')
        else:
            if self.use_function(state) != Constants.CANCELLED:
                state.player_inventory.inventory.remove(self.owner)    #destroy after use, unless cancelled

    def drop(self, state):
        state.objects.append(self.owner)
        state.player_inventory.inventory.remove(self.owner)
        self.owner.x = state.player.x
        self.owner.y = state.player.y
        state.status_panel.message('You drop a ' + self.owner.name + '.', libtcod.turquoise)
