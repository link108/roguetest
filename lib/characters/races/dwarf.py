__author__ = 'cmotevasselani'

from base_race import BaseRace
from lib.characters.fighter import Fighter
from lib.constants.constants import Constants


class Dwarf(BaseRace):
  @staticmethod
  def get_fighter_component():
    return Fighter(hp=130, defense=1, power=4, xp=0)

