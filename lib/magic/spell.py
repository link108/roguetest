__author__ = 'cmotevasselani'

from lib.constants.constants import Constants
from lib.magic.all_spells import *


class Spell:
  def __init__(self, name, spell_string):
    self.name = name
    spell_info = spell_string.split('_XXX_')
    self.mp_cost = int(spell_info[0])
    self.range = int(spell_info[1])
    self.power = int(spell_info[2])
    self.description = spell_info[3]
    self.magic_class = spell_info[4]
    self.use_function = getattr(eval(self.magic_class), self.name)

  # def set_use_function(self, use_function):
  #     spell.set_use_function(getattr(eval(spell.magic_class), spell_name))
  #     self.use_function = use_function

  def cast(self, state, owner):
    if self.use_function(state) != Constants.CANCELLED:
      owner.caster.deplete_mp(self.mp_cost)

      # def learn(self, state):
      #     self.range
