__author__ = 'cmotevasselani'

from lib import libtcodpy as libtcod
from lib.consoles.menu import Menu
from lib.map_constants import MapConstants

INVENTORY_WIDTH = 50


class Inventory:

    def __init__(self, status_panel, objects, player):
        self.status_panel = status_panel
        self.inventory = []
        self.objects = objects
        self.menu = Menu()
        self.player = player

    def get_status_panel(self):
        return self.status_panel

    def inventory_menu(self, header, util):
        #show a menu with each item of the inventory as an option
        if len(self.inventory) == 0:
            options = ['Inventory is empty.']
        else:
            options = [item.name for item in self.inventory]

        index = self.menu.display_menu(header, options, INVENTORY_WIDTH, util.con, MapConstants.SCREEN_WIDTH, MapConstants.SCREEN_HEIGHT)

        if index is None or len(self.inventory) == 0: return None;
        return self.inventory[index].item

    def drop(self, object):
        self.objects.append(object.owner)
        self.inventory.remove(object.owner)
        object.owner.x = self.player.x
        object.owner.y = self.player.y
        self.status_panel.message('You drop a ' + object.owner.name + '.', libtcod.turquoise)


