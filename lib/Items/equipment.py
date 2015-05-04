__author__ = 'cmotevasselani'

from lib.random_libs import libtcodpy as libtcod

from lib.constants.equipment_constants import EquipmentConstants
from lib.utility_functions.util import Util
from lib.items.item import Item
from lib.utility_functions.object import Object


class Equipment:
  def __init__(self, name=None, equipment_string=None):
    self.item = Item()
    self.is_equipped = False
    if name and equipment_string:
      self.name = name
      self.display_name = self.name.replace('_', ' ')
      equipment_info = equipment_string.strip().split('_XXX_')
      self.power_bonus = int(equipment_info[0])
      self.defense_bonus = int(equipment_info[1])
      self.hp_bonus = int(equipment_info[2])
      self.representation = equipment_info[3]
      self.color = getattr(libtcod, equipment_info[4])
      self.slot = getattr(EquipmentConstants, equipment_info[5])
      self.always_visible = bool(equipment_info[6])

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
      old_equipment.equipment.dequip(state)
    self.is_equipped = True
    state.status_panel.message('Equiped ' + self.owner.name + ' on ' + self.slot + '.', libtcod.light_green)

  def get_equipment(self, x, y):
    return Object(x, y,
                  self.representation,
                  self.display_name,
                  self.color,
                  equipment=self,
                  always_visible=True)

  def get_info(self, state):
    return "Power Bonus: " + str(self.power_bonus) + ", Defense Bonus: " + str(self.defense_bonus) + ", HP Bonus: " + str(self.hp_bonus)

