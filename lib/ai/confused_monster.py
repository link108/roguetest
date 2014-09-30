__author__ = 'cmotevasselani'

from lib import libtcodpy as libtcod

class ConfusedMonster:

    CONFUSE_NUM_TURNS = 5

    def __init__(self, old_ai, util, num_turns=CONFUSE_NUM_TURNS):
        self.old_ai = old_ai
        self.num_turns = num_turns
        self.util = util

    def take_turn(self, util):
        # Move randomly
        if self.num_turns > 0:
            self.owner.move(util.objects, util.game_map, libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))
            self.num_turns -= 1
        else:
            # reset to old AI
            self.owner.ai = self.old_ai
            util.status_panel.message('The ' + self.owner.name + ' is no longer confused!', libtcod.red)
