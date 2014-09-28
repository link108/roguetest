__author__ = 'cmotevasselani'

from lib import libtcodpy as libtcod
from lib import item


class PotionFunctions:

    HEAL_AMOUNT = 4

    @staticmethod
    def cast_heal(player, status_panel):
        if player.fighter.hp == player.fighter.max_hp:
            status_panel.message('You are already at full health.', libtcod.red)
            return item.CANCELLED
        status_panel.message('Your wounds start to feel better', libtcod.light_violet)
        player.fighter.heal(PotionFunctions.HEAL_AMOUNT)
