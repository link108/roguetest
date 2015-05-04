__author__ = 'cmotevasselani'

from lib.random_libs import libtcodpy as libtcod
from lib.utility_functions.util import Util
from lib.constants.constants import Constants


class FrostMagic:
  @staticmethod
  def frost_shock(state):
    monster = Util.target_monster(state, Constants.FROST_SHOCK_RANGE)
    if monster is None:
      state.status_panel.message('No enemy is close enough or none selected', libtcod.red)
      return Constants.CANCELLED
    state.status_panel.message('You Frost Shock: ' + monster.name + '! The damage done is '
                               + str(Constants.FROST_SHOCK_DAMAGE) + ' hp.', libtcod.light_blue)
    monster.fighter.take_damage(Constants.FROST_SHOCK_DAMAGE, state)


