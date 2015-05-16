from lib.random_libs import libtcodpy as libtcod

__author__ = 'cmotevasselani'

from lib.consoles.menu import Menu
from lib.constants.constants import Constants
from lib.utility_functions.util import Util


class SpellInventory:
  def __init__(self, state):
    self.status_panel = state.status_panel
    self.menu = Menu()
    self.player = state.player
    self.spells = state.player.caster.spells

  def spell_menu(self, header, state):
    # show a menu with each item of the inventory as an option
    if len(self.spells) == 0:
      options = ['You have no spells.']
    else:
      options = []
      for spell_name in state.player.caster.spells:
        spell = state.magic.spells[spell_name]
        text = spell_name + ' : ' + spell.description + ', mp cost: ' + str(spell.mp_cost) + ', spell range: ' + str(
          spell.range) + \
               ', spell power: ' + str(spell.power)
        options.append(text)

    index = self.menu.display_menu_return_index(header, options, Constants.INVENTORY_WIDTH, state.con)
    if index is not None:
      spell_name = options[index].split(' : ')[0]

    if index is None or len(self.spells) == 0:
      state.set_player_action(Constants.NOT_VALID_KEY)
      Util.refresh(state)
      return None
    return state.magic.spells[spell_name]

    # TODO either remove or add forget spell functionality (should have reason behind adding it)
    # def drop(self, object):
    #     self.objects.append(object.owner)
    #     self.inventory.remove(object.owner)
    #     object.owner.x = self.player.x
    #     object.owner.y = self.player.y
    #     self.status_panel.message('You drop a ' + object.owner.name + '.', libtcod.turquoise)


