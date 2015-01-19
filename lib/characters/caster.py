__author__ = 'cmotevasselani'

from lib.magic.magic import Magic

class Caster:

    def __init__(self, mp, spell_power, spells):
        self.base_max_mp = mp
        self.mp = mp
        self.spell_power = spell_power
        self.spells = spells

    # @property def power(self):
    #     bonus = sum(equipment.power_bonus for equipment in Util.get_all_equiped(self.state, self.owner))
    #     return self.base_power + bonus
    #
    # @property
    # def defense(self):
    #     bonus = sum(equipment.defense_bonus for equipment in Util.get_all_equiped(self.state, self.owner))
    #     return self.base_defense + bonus

    def max_mp(self, state):
        # bonus = sum(equipment.hp_bonus for equipment in Util.get_all_equiped(self.state, self.owner))
        return self.base_max_mp

    def deplete_mp(self, amount):
        if amount > 0:
            self.mp -= amount
            if self.mp < 0:
                self.mp = 0

    # def cast_spell(self, spell_name):
    #     if spell_name in self.spells:
    #         spell = Magic.spells[spell_name]


