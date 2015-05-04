__author__ = 'cmotevasselani'

from lib.random_libs import libtcodpy as libtcod
from lib.constants.monster_constants import MonsterConstants
from lib.utility_functions.util import Util
from lib.utility_functions.object import Object


class MonsterPlacer:
  @staticmethod
  def place_monsters(state, game_map, room, objects):
    max_monsters_table = [[2, 0], [3, 3], [5, 5]]
    max_monsters = Util.from_dungeon_level(state, max_monsters_table)

    # choose random number of monsters
    monster_chances = {
      MonsterConstants.ORC: 80,
      MonsterConstants.TROLL: Util.from_dungeon_level(state, [[15, 3], [30, 5], [60, 7]])
    }
    num_monsters = libtcod.random_get_int(0, 0, max_monsters)
    for i in range(num_monsters):
      # choose random spot for this monster
      x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
      y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)

      if not game_map.is_blocked(objects, x, y):
        choice = Util.random_choice(monster_chances)
        monster = state.monsters.get_data_object(choice)
        objects.append(monster.get_monster(x, y))
