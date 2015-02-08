__author__ = 'cmotevasselani'

from base_class import BaseClass
from lib.characters.caster import Caster
from lib.constants.constants import Constants

class Archer(BaseClass):

    @staticmethod
    def get_caster_component():
        return Caster(mp=10, spell_power=4, spells=[Constants.FROST_SHOCK])
