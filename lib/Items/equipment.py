__author__ = 'cmotevasselani'

from lib.random_libs import libtcodpy as libtcod
from lib.utility_functions.util import Util


class Equipment:

    def __init__(self, state, slot):
        self.state = state
        self.slot = slot
        self.is_equipped = False

    def toggle_equipment(self):
        if self.is_equipped:
            self.dequip()
        else:
            self.equip()

    def dequip(self):
        self.is_equipped = False
        self.state.status_panel.message('Dequiped ' + self.owner.name + ' from ' + self.slot + '.', libtcod.light_yellow)

    def equip(self):
        old_equipment = Util.get_equipped_in_slot(self.state, self.slot)
        if old_equipment is not None:
            old_equipment.equipment.dequip()
        self.is_equipped = True
        self.state.status_panel.message('Equiped ' + self.owner.name + ' on ' + self.slot + '.', libtcod.light_green)

