__author__ = 'cmotevasselani'

from lib.constants.constants import Constants
from lib.constants.map_constants import MapConstants
from lib.constants.equipment_constants import EquipmentConstants
from lib.utility_functions.object import Object
from lib.random_libs import libtcodpy as libtcod
from lib.items.inventory import Inventory
from lib.magic.spell_inventory import SpellInventory
from lib.consoles.menu import Menu
from lib.constants.item_constants import ItemConstants
from classes.warrior import Warrior
from classes.mage import Mage
from classes.archer import Archer
from races.elf import Elf
from races.human import Human
from races.dwarf import Dwarf
from fighter import Fighter

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
    self.state.player = Object(0, 0, '@', Constants.PLAYER, libtcod.white, blocks=True, fighter=self.fighter_component,
                               caster=self.caster_component)
    self.state.player.level = 1
    self.state.player_inventory = Inventory(self.state)
    self.state.player_spell_inventory = SpellInventory(self.state)
    self.get_starting_equipment()

  def choose_class(self):
    while (self.player_class == None):
      self.player_class = self.menu.display_menu_return_item('Choose a class:',
                                                             [Constants.WARRIOR, Constants.MAGE, Constants.ARCHER], 30,
                                                             self.state.con,
                                                             override_height=MapConstants.MENU_HEIGHT_ADDITION)
    self.state.player_class = self.player_class

  def choose_race(self):
    while (self.player_race == None):
      self.player_race = self.menu.display_menu_return_item('Choose a race:',
                                                            [Constants.ELF, Constants.HUMAN, Constants.DWARF], 30,
                                                            self.state.con,
                                                            override_height=MapConstants.MENU_HEIGHT_ADDITION)
    self.state.player_race = self.player_race

  def get_caster_component(self):
    self.caster_component = getattr(eval(self.player_class), 'get_caster_component')()

  def get_fighter_component(self):
    self.fighter_component = getattr(eval(self.player_race), 'get_fighter_component')()

  # TODO Make this fit the class / race better
  def get_starting_equipment(self):
    equipment_component = self.state.equipment.get_data_object(EquipmentConstants.DAGGER)
    item = equipment_component.get_equipment(0, 0)
    self.state.player_inventory.inventory.append(item)
    equipment_component.equip(self.state)


