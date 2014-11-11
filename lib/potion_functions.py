__author__ = 'cmotevasselani'

from lib import libtcodpy as libtcod
from lib.constants import Constants


class PotionFunctions:


    @staticmethod
    def cast_heal(state):
        if state.player.fighter.hp == state.player.fighter.max_hp:
            state.status_panel.message('You are already at full health.', libtcod.red)
            return Constants.CANCELLED
        state.status_panel.message('Your wounds start to feel better', libtcod.light_violet)
        state.player.fighter.heal(Constants.HEAL_AMOUNT)
