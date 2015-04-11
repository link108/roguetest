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
from lib.consoles.menu import Menu
from classes.warrior import Warrior
from classes.mage import Mage
from classes.archer import Archer
from races.elf import Elf
from races.human import Human
from races.dwarf import Dwarf


# def player_death(player, state):
#     #the game ended, yasd?
#     # global game_state
#     state.status_panel.message('You died!', libtcod.white)
#     Util.set_game_state(Constants.DEAD)
#     #player is a corpse
#     state.player.char = '%'
#     state.player.color = libtcod.dark_red

class CreateCharacter:

    def __init__(self, state):
        self.state = state
        self.menu = Menu()
        self.player_class = None
        self.player_race = None
        self.caster_component = None
        self.fighter_component = None
        self.choose_race()
        self.choose_class()
        self.get_caster_component()
        self.get_fighter_component()
        self.state.player = Object(0, 0, '@', Constants.PLAYER, libtcod.white, blocks=True, fighter=self.fighter_component, caster=self.caster_component)
        self.state.player.level = 1
        self.state.player_inventory = Inventory(self.state)
        self.state.player_spell_inventory = SpellInventory(self.state)
        self.get_starting_equipment()

    def choose_class(self):
        # self.player_class = self.menu.display_menu_return_item('Choose a class:', [Constants.WARRIOR, Constants.MAGE, Constants.ARCHER], 30, self.state.con)
        while(self.player_class == None):
            self.player_class = self.menu.display_menu_return_item('Choose a class:', [Constants.WARRIOR, Constants.MAGE, Constants.ARCHER], 30, self.state.con)
        self.state.player_class = self.player_class

    def choose_race(self):
        while(self.player_race == None):
            self.player_race = self.menu.display_menu_return_item('Choose a race:', [Constants.ELF, Constants.HUMAN, Constants.DWARF], 30, self.state.con)
        self.state.player_race = self.player_race

    def get_caster_component(self):
        self.caster_component = getattr(eval(self.player_class), 'get_caster_component')()
        # self.caster_component = Caster(mp=10, spell_power=4, spells=[Constants.FROST_SHOCK])

    def get_fighter_component(self):
        self.fighter_component = getattr(eval(self.player_race), 'get_fighter_component')()
        # self.fighter_component = Fighter(hp=100, defense=1, power=4, xp=0, death_function=player_death)

    def get_starting_equipment(self):
        equipment_component = Equipment(slot=Constants.RIGHT_HAND, power_bonus=2)
        obj = Object(0, 0, '-', MapConstants.DAGGER, libtcod.red, equipment=equipment_component, always_visible=True)
        self.state.player_inventory.inventory.append(obj)
        equipment_component.equip(self.state)


