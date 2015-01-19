from lib.random_libs import libtcodpy as libtcod

__author__ = 'cmotevasselani'

from lib.consoles.menu import Menu
from lib.constants.constants import Constants
from lib.utility_functions.util import Util



class Inventory:

    def __init__(self, state):
        self.status_panel = state.status_panel
        self.inventory = []
        self.objects = state.objects
        self.menu = Menu()
        self.player = state.player

    # def get_status_panel(self):
    #     return self.status_panel

    def inventory_menu(self, header, state):
        #show a menu with each item of the inventory as an option
        if len(self.inventory) == 0:
            options = ['Inventory is empty.']
        else:
            options = []
            for item in state.player_inventory.inventory:
                text = item.name
                if item.equipment and item.equipment.is_equipped:
                    text = text + ' (on ' + item.equipment.slot + ')'
                options.append(text)



        index = self.menu.display_menu(header, options, Constants.INVENTORY_WIDTH, state.con)

        if index is None or len(self.inventory) == 0:
            Util.set_player_action(Constants.DID_NOT_TAKE_TURN)
            return None;
        return self.inventory[index].item

    # def drop(self, object):
    #     self.objects.append(object.owner)
    #     self.inventory.remove(object.owner)
    #     object.owner.x = self.player.x
    #     object.owner.y = self.player.y
    #     self.status_panel.message('You drop a ' + object.owner.name + '.', libtcod.turquoise)


