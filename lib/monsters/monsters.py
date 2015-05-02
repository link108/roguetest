__author__ = 'cmotevasselani'

import copy
from lib.constants.constants import Constants
from lib.monsters.monster import Monster


class Monsters:

    def __init__(self):
        self.monsters = {}
        self.init_monsters()

    def init_monsters(self):
        with open(Constants.MONSTER_FILE) as f:
            monster_file = f.readlines()
        for line in monster_file:
            if '#' not in line:
                line_array = line.split(' ')
                monster_name = line_array[0]
                monster_stuff = line_array[1]
                monster = Monster(monster_name, monster_stuff)
                # spell.set_use_function(getattr(eval(spell.magic_class), spell_name))
                self.monsters[monster_name] = monster

    def get_monster(self, monster_name):
        return copy.deepcopy(self.monsters[monster_name])

