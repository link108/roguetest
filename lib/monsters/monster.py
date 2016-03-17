__author__ = 'cmotevasselani'

from lib.random_libs import libtcodpy as libtcod

from lib.characters.fighter import Fighter
from lib.utility_functions.object import Object


# Must include all ai modules here
from lib.ai.basic_monster import BasicMonster
from lib.ai.smarter_monster import SmarterMonster


class Monster:
  def __init__(self, name=None, monster_string=None):
    if name and monster_string:
      self.name = name
      monster_info = monster_string.strip().split('_XXX_')
      self.hp = int(monster_info[0])
      self.defense = int(monster_info[1])
      self.power = int(monster_info[2])
      self.xp = int(monster_info[3])
      self.max_xp = self.xp
      self.score = int(monster_info[4])
      self.ai = monster_info[5]
      self.representation = monster_info[6]
      self.blocks = bool(monster_info[7])
      self.color = getattr(libtcod, monster_info[8])

  def get_fighter_component(self):
    return Fighter(hp=self.hp,
                   defense=self.defense,
                   power=self.power,
                   xp=self.xp,
                   score=self.score)

  def get_ai_component(self):
    return eval(self.ai)()

  def create_at_location(self, x, y):
    return Object(x, y,
                  self.representation,
                  self.name,
                  self.color,
                  blocks=self.blocks,
                  fighter=self.get_fighter_component(),
                  ai=self.get_ai_component())

