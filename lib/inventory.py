__author__ = 'cmotevasselani'

from lib.consoles.menu import Menu

INVENTORY_WIDTH = 50


class Inventory:

    def __init__(self, status_panel, objects):
        self.status_panel = status_panel
        self.inventory = []
        self.objects = objects
        self.menu = Menu()

    def get_status_panel(self):
        return self.status_panel

    def inventory_menu(self, header, con, screen_width, screen_height):
        #show a menu with each item of the inventory as an option
        if len(self.inventory) == 0:
            options = ['Inventory is empty.']
        else:
            options = [item.name for item in self.inventory]

        index = self.menu.display_menu(header, options, INVENTORY_WIDTH, con, screen_width, screen_height)

        if index is None or len(self.inventory) == 0: return None;
        return self.inventory[index].item