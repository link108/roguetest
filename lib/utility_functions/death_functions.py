__author__ = 'cmotevasselani'

from lib import libtcodpy as libtcod
from lib.constants import Constants
from lib.util import Util

class DeathFunctions:

    @staticmethod
    def player_death(player, state):
        #the game ended, yasd?
        # global game_state
        state.status_panel.message('You died!', libtcod.white)
        Util.set_game_state(Constants.DEAD)
        #player is a corpse
        state.player.char = '%'
        state.player.color = libtcod.dark_red

    @staticmethod
    def monster_death(monster, state):
        #monster turns into a corpse, does not block, cant be attacked, does not move
        state.status_panel.message(monster.name.capitalize() + ' is dead!', libtcod.white)
        monster.char = '%'
        monster.color = libtcod.dark_red
        monster.blocks = False
        monster.fighter = None
        monster.ai = None
        monster.name = 'remains of ' + monster.name
        monster.send_to_back(state.objects)


