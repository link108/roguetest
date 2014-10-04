__author__ = 'cmotevasselani'

from lib import libtcodpy as libtcod
CANCELLED = 'cancelled'


class Item:

    def __init__(self, use_function = None):
        self.use_function = use_function

    # an item that can be picked up and used.
    def pick_up(self, inventory):
        #add to the player's inventory and remove from the map
        if len(inventory.inventory) >= 26:
            inventory.status_panel.message('Your inventory is full, cannot pick up ' + self.owner.name + '.', libtcod.red)
        else:
            inventory.inventory.append(self.owner)
            inventory.objects.remove(self.owner)
            inventory.status_panel.message('You picked up a ' + self.owner.name + '!', libtcod.green)

    def use(self, util):
        #call use_function if defined
        if self.use_function is None:
            util.status_panel.message('The ' + self.owner.name + ' cannot be used.')
        else:
            if self.use_function(util) != CANCELLED:
                util.player_inventory.inventory.remove(self.owner)    #destroy after use, unless cancelled
