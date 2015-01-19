__author__ = 'cmotevasselani'

from lib.random_libs import libtcodpy as libtcod
from lib.utility_functions.util import Util


class Equipment:

    def __init__(self, slot, power_bonus=0, defense_bonus=0, hp_bonus=0):
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.hp_bonus = hp_bonus
        self.slot = slot
        self.is_equipped = False

    def toggle_equipment(self, state):
        if self.is_equipped:
            self.dequip(state)
        else:
            self.equip(state)

    def dequip(self, state):
        self.is_equipped = False
        state.status_panel.message('Dequiped ' + self.owner.name + ' from ' + self.slot + '.', libtcod.light_yellow)

    def equip(self, state):
        old_equipment = Util.get_equipped_in_slot(state, self.slot)
        if old_equipment is not None:
            old_equipment.equipment.dequip()
        self.is_equipped = True
        state.status_panel.message('Equiped ' + self.owner.name + ' on ' + self.slot + '.', libtcod.light_green)

