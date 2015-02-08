from lib.random_libs import libtcodpy as libtcod
from lib.utility_functions.util import Util
from death_functions import DeathFunctions

__author__ = 'cmotevasselani'


class Fighter:
    #combat related properties and methods (npcs, monsters, player)
    def __init__(self, hp, defense, power, xp):
        self.level = 1
        self.base_max_hp = hp
        self.xp = xp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power

    def power(self, state):
        bonus = sum(equipment.power_bonus for equipment in Util.get_all_equiped(state, self.owner))
        return self.base_power + bonus

    def defense(self, state):
        bonus = sum(equipment.defense_bonus for equipment in Util.get_all_equiped(state, self.owner))
        return self.base_defense + bonus

    def max_hp(self, state):
        bonus = sum(equipment.hp_bonus for equipment in Util.get_all_equiped(state, self.owner))
        return self.base_max_hp + bonus

    def take_damage(self, damage, state):
        #apply damage if possible
        if damage > 0:
            self.hp -= damage
            if self.hp <= 0:
                DeathFunctions.death(self.owner, state)
                if self.owner != state.player:
                    state.player.fighter.xp += self.xp


    def attack(self, target, state):
        #simple formula for attack damage
        damage = self.power(state) - target.fighter.defense(state)

        if damage > 0:
            #make the target take some damage
            state.status_panel.message(self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points', libtcod.white)
            target.fighter.take_damage(damage, state)
        else:
            state.status_panel.message(self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!', libtcod.gray)

    def heal(self, amount, state):
        self.hp += amount
        # dont go over max hp limit
        max_hp = self.max_hp(state)
        if self.hp > max_hp:
            self.hp = max_hp
