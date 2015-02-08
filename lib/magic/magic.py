__author__ = 'cmotevasselani'

from lib.constants.constants import Constants
from lib.magic.spell import Spell
from lib.magic.frost_magic import FrostMagic

class Magic:

    def __init__(self):
        self.spells = {}
        self.init_spells()

    def init_spells(self):
        with open(Constants.SPELL_FILE) as f:
            spell_file = f.readlines()
        for line in spell_file:
            if '#' not in line:
                line_array = line.split(' ')
                spell_name = line_array[0]
                spell_stuff = line_array[1]
                spell = Spell(spell_name, spell_stuff)
                # spell.set_use_function(getattr(eval(spell.magic_class), spell_name))
                self.spells[spell_name] = spell


