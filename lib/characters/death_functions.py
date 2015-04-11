__author__ = 'cmotevasselani'

from lib.random_libs import libtcodpy as libtcod
from lib.constants.constants import Constants
from lib.utility_functions.util import Util

class DeathFunctions:

    @staticmethod
    def get_death_function(name, state):
        if name == Constants.PLAYER:
            return DeathFunctions.player_death
        else:
            return DeathFunctions.monster_death

    @staticmethod
    def death(owner, state):
        if owner.name == Constants.PLAYER:
            DeathFunctions.player_death(owner, state)
        else:
            DeathFunctions.monster_death(owner, state)

    @staticmethod
    def monster_death(monster, state):
        #monster turns into a corpse, does not block, cant be attacked, does not move
        state.status_panel.message(monster.name.capitalize() + ' is dead! You gain ' + str(monster.fighter.xp) + ' xp!', libtcod.white)
        state.score += monster.fighter.score
        monster.char = '%'
        monster.color = libtcod.dark_red
        monster.blocks = False
        monster.fighter = None
        monster.ai = None
        monster.name = 'remains of ' + monster.name
        monster.send_to_back(state.objects)

    @staticmethod
    def player_death(player, state):
        #the game ended, yasd?
        # global game_state
        state.status_panel.message('You died!', libtcod.red)
        Util.set_game_state(Constants.DEAD)
        #player is a corpse
        state.player.char = '%'
        state.player.color = libtcod.dark_red

