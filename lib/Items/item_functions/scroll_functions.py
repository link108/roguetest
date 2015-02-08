__author__ = 'cmotevasselani'

from lib.random_libs import libtcodpy as libtcod
from lib.utility_functions.util import Util
from lib.constants.constants import Constants
from lib.ai.confused_monster import ConfusedMonster

###### ScrollFunctions

class ScrollFunctions:

    @staticmethod
    def cast_fireball(state):
        # TODO: Add range check
        x, y = Util.target_tile(state)
        state.game_map.get_map()[x][y].set_targeted(False)
        for object in state.objects:
            if object.distance(x,y) <= Constants.FIREBALL_RADIUS and object.fighter:
                state.status_panel.message('You sling a fireball at: ' + object.name + ' with a BAMboosh! The damage done is '
                                    + str(Constants.FIREBALL_DAMAGE) + ' hp.', libtcod.light_blue)
                object.fighter.take_damage(Constants.FIREBALL_DAMAGE, state)

    def cast_confuse(state):
        # monster = Constants.closest_monster(util, Constants.CONFUSE_RANGE)
        monster = Util.target_monster(state, Constants.CONFUSE_RANGE)
        if monster is None:
            state.status_panel.message('No enemy is close enough to confuse', libtcod.red)
            return Constants.CANCELLED
        old_ai = monster.ai
        monster.ai = ConfusedMonster(old_ai, state)
        monster.clear(state.con)
        monster.ai.owner = monster
        state.status_panel.message('The eyes of the ' + monster.name + ' look vacant, as he starts to stumble around!', libtcod.light_green)

    def cast_lightning(state):
        monster = Util.closest_monster(state, Constants.LIGHTNING_RANGE)
        if monster is None:
            state.status_panel.message('No enemy is close enough to strike with lightning', libtcod.red)
            return Constants.CANCELLED
        state.status_panel.message('A lightning bolt strikes the ' + monster.name + ' with a ZAP! The damage done is '
                            + str(Constants.LIGHTNING_DAMAGE) + ' hp.', libtcod.light_blue)
        monster.fighter.take_damage(Constants.LIGHTNING_DAMAGE, state)
