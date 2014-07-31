__author__ = 'cmotevasselani'

from lib import libtcodpy as libtcod


class Item:

    # an item that can be picked up and used.
    def pick_up(self, inventory):
        #add to the player's inventory and remove from the map
        if len(inventory.inventory) >= 26:
            inventory.status_panel.message('Your inventory is full, cannot pick up ' + self.owner.name + '.', libtcod.red)
        else:
            inventory.inventory.append(self.owner)
            inventory.objects.remove(self.owner)
            inventory.status_panel.message('You picked up a ' + self.owner.name + '!', libtcod.green)
