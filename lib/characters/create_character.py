__author__ = 'cmotevasselani'

from caster import Caster
from fighter import Fighter
from lib.constants.constants import Constants
from lib.constants.map_constants import MapConstants
from lib.utility_functions.util import Util
from lib.utility_functions.object import Object
from lib.random_libs import libtcodpy as libtcod
from lib.items.inventory import Inventory
from lib.items.equipment import Equipment
from lib.magic.spell_inventory import SpellInventory

def player_death(player, state):
    #the game ended, yasd?
    # global game_state
    state.status_panel.message('You died!', libtcod.white)
    Util.set_game_state(Constants.DEAD)
    #player is a corpse
    state.player.char = '%'
    state.player.color = libtcod.dark_red

class CreateCharacter:

    def __init__(self, state):
        self.caster_component = None
        self.fighter_component = None
        self.choose_race()
        self.choose_class()
        state.player = Object(0, 0, '@', 'player', libtcod.white, blocks=True, fighter=self.fighter_component, caster=self.caster_component)
        state.player.level = 1
        state.player_inventory = Inventory(state)
        state.player_spell_inventory = SpellInventory(state)
        self.get_starting_equipment('whatever', state)

    def choose_class(self):
        self.caster_component = Caster(mp=10, spell_power=4, spells=[Constants.FROST_SHOCK])

    def choose_race(self):
        self.fighter_component = Fighter(hp=100, defense=1, power=4, xp=0, death_function=player_death)

    def get_starting_equipment(self, character_class, state):
        equipment_component = Equipment(slot=Constants.RIGHT_HAND, power_bonus=2)
        obj = Object(0, 0, '-', MapConstants.DAGGER, libtcod.red, equipment=equipment_component, always_visible=True)
        state.player_inventory.inventory.append(obj)
        equipment_component.equip(state)


