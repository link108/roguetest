__author__ = 'cmotevasselani'

from lib import libtcodpy as libtcod
from lib import item


class PotionFunctions:

    HEAL_AMOUNT = 4

    @staticmethod
    def cast_heal(util):
        if util.player.fighter.hp == util.player.fighter.max_hp:
            util.status_panel.message('You are already at full health.', libtcod.red)
            return item.CANCELLED
        util.status_panel.message('Your wounds start to feel better', libtcod.light_violet)
        util.player.fighter.heal(PotionFunctions.HEAL_AMOUNT)
