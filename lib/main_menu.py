__author__ = 'cmotevasselani'

import shelve
from lib.random_libs import libtcodpy as libtcod
from lib.map_components.map import Map
from lib.utility_functions.state import State
from lib.items.inventory import Inventory
from lib.constants.map_constants import MapConstants
from lib.constants.constants import Constants
from lib.utility_functions.util import Util
from lib.consoles.menu import Menu
from lib.magic.spell_inventory import SpellInventory
from lib.characters.create_character import CreateCharacter
from lib.high_scores.high_scores import HighScores
from lib.utility_functions.datafile_loader import DatafileLoader
from lib.magic.spell import Spell
from lib.items.item import Item
from lib.items.equipment import Equipment
from lib.monsters.monster import Monster
from lib.utility_functions.input.input import Input


class MainMenu:

  def __init__(self, args):
    self.state = State()
    self.state.debug = bool(args.debug)
    self.state.god_mode = bool(args.god_mode)
    self.menu = Menu()
    self.state.magic = DatafileLoader(data_file=Constants.SPELL_FILE, data_class=Spell, map_name="spells")
    self.state.items = DatafileLoader(data_file=Constants.ITEM_FILE, data_class=Item, map_name="items")
    self.state.monsters = DatafileLoader(data_file=Constants.MONSTER_FILE, data_class=Monster, map_name="monsters")
    self.state.equipment = DatafileLoader(data_file=Constants.EQUIPMENT_FILE, data_class=Equipment, map_name="equipments")
    self.state.high_scores = HighScores()

  def main_menu(self):
    # img = libtcod.image_load('rl_image.png')
    # show the background image, at twice the regular console resolution
    while not libtcod.console_is_window_closed():
      # libtcod.image_blit_2x(img, 0, 0, 0)
      choice = self.menu.display_menu_return_index('', ['Play a new game', 'Continue last game',
                                                        'Battle (work in progress)', 'High Scores', 'Quit'], 30,
                                                   self.state.con)
      if choice == 0:
        self.new_game()
        self.play_game()
      elif choice == 1:
        try:
          self.load_game()
        except:
          self.message_box('No saved game to load', 24)
          continue
        self.play_game()
      elif choice == 2:
        self.battle()
        self.play_game()
      elif choice == 3:
        self.show_high_scores()
      elif choice == 4:
        break

  def show_high_scores(self):
    self.state.high_scores.show_high_scores(self.state, self.menu)

  def message_box(self, message, size=50):
    self.menu.display_menu_return_index(message, [], size, self.state.con)

  def setup_game(self):
    self.state.status_panel.game_messages = []
    self.state.status_panel.message('Welcome stranger! Prepare to perish in the Tombs of the Ancient Kings.',
                                    libtcod.red)
    self.state.dungeon_level = 0
    self.state.turn = 0
    self.state.score = 0
    self.choose_class(self.state)
    self.state.objects_map[self.state.dungeon_level] = [self.state.player]
    self.state.objects = self.state.objects_map[self.state.dungeon_level]


  def battle(self):
    self.setup_game()
    self.state.game_map = Map(self.state)
    self.state.game_map.generate_battle_map(self.state)
    self.state.game_map.set_game_map(self.state.dungeon_level)
    self.initialize_fov(self.state.dungeon_level)
    self.state.set_player_action(None)

  def choose_class(self, state):
    CreateCharacter(state)

  def new_game(self):
    self.setup_game()
    self.state.game_map = Map(self.state)
    self.state.game_map.generate_map(self.state, self.state.dungeon_level)
    self.state.game_map.set_game_map(self.state.dungeon_level)
    self.initialize_fov(self.state.dungeon_level)
    self.state.set_player_action(None)

  def initialize_fov(self, dungeon_level):
    self.state.fov_map_map[dungeon_level] = libtcod.map_new(MapConstants.MAP_WIDTH, MapConstants.MAP_HEIGHT)
    libtcod.console_clear(self.state.con)
    for y in range(MapConstants.MAP_HEIGHT):
      for x in range(MapConstants.MAP_WIDTH):
        libtcod.map_set_properties(self.state.fov_map_map[dungeon_level], x, y,
                                   not self.state.game_map.is_blocked_sight(self.state.objects, x, y),
                                   not self.state.game_map.is_blocked_sight(self.state.objects, x, y))
    self.state.fov_map = self.state.fov_map_map[dungeon_level]

  def play_game(self):
    self.state.set_game_state(Constants.PLAYING)
    self.state.set_player_action(None)
    self.state.fov_recompute = True

    while not libtcod.console_is_window_closed():
      self.state.turn += 1
      Util.render_all(self.state)
      libtcod.console_flush()
      Util.check_level_up(self.state)
      for object in self.state.objects:
        object.clear(self.state.con)
      self.state.set_player_action(Constants.DID_NOT_TAKE_TURN)
      while self.state.get_player_action() == Constants.DID_NOT_TAKE_TURN:
        Input.handle_keys(self.state)

      player_action = self.state.get_player_action()
      if player_action == Constants.EXIT or self.state.player.color == libtcod.dark_red:
        self.save_game()
        break

      if self.state.get_game_state() == Constants.PLAYING and self.state.get_player_action() != Constants.DID_NOT_TAKE_TURN:
        for object in self.state.objects:
          if object.ai:
            object.ai.take_turn(self.state)
      if player_action == Constants.NEXT_LEVEL:
        self.next_level()
      elif player_action == Constants.PREVIOUS_LEVEL:
        self.previous_level()
      elif player_action == Constants.EXIT or self.state.player.color == libtcod.dark_red:
        Util.render_all(self.state)
        self.save_game()
        break
      self.state.status_panel.message('###### Turn ' + str(self.state.turn) + ' has ended')

  def previous_level(self):
    up_stairs_id = Util.get_padded_coords(self.state.player.x, self.state.player.y)
    down_stairs_id = self.follow_stairs(MapConstants.UP_STAIRS_OBJECT, up_stairs_id, self.state.dungeon_level)
    self.state.player.x, self.state.player.y = Util.get_coords_from_padded_coords(down_stairs_id)
    if self.state.dungeon_level == 0:
      self.state.set_player_action(Constants.EXIT)
      return
    else:
      self.state.dungeon_level -= 1
    self.state.objects = self.state.objects_map[self.state.dungeon_level]
    self.state.game_map.set_game_map(self.state.dungeon_level)
    # TODO Make fov_map container class
    self.state.fov_map = self.state.fov_map_map[self.state.dungeon_level]
    self.initialize_fov(self.state.dungeon_level)
    self.state.set_player_action(None)
    self.state.fov_recompute = True

  def follow_stairs(self, type_entered, stairs_id_entered, stairs_entered_dungeon_level):
    other_stairs_id = self.state.stairs[stairs_entered_dungeon_level][type_entered][stairs_id_entered]
    return other_stairs_id

  def next_level(self):
    self.state.dungeon_level += 1
    self.state.status_panel.message('You take a moment to rest and recover 50% health', libtcod.violet)
    self.state.player.fighter.heal(self.state.player.fighter.max_hp(self.state) / 2, self.state)
    self.state.status_panel.message('and now you descend into the depths of the dungeon', libtcod.red)
    if self.state.dungeon_level in self.state.game_map.complete_game_map:
      self.state.game_map.set_game_map(self.state.dungeon_level)
      down_stairs_id = Util.get_padded_coords(self.state.player.x, self.state.player.y)
      up_stairs_id = self.follow_stairs(MapConstants.DOWN_STAIRS_OBJECT, down_stairs_id, self.state.dungeon_level - 1)
      self.state.player.x, self.state.player.y = Util.get_coords_from_padded_coords(up_stairs_id)
    else:
      self.state.objects_map[self.state.dungeon_level] = [self.state.player]
      self.state.game_map.generate_map(self.state, self.state.dungeon_level)
      self.state.score += self.state.dungeon_level * 10
    self.state.objects = self.state.objects_map[self.state.dungeon_level]
    self.initialize_fov(self.state.dungeon_level)
    self.state.set_player_action(None)
    self.state.fov_recompute = True
    Util.render_all(self.state)

  def save_game(self):
    file = shelve.open(Constants.SAVE_FILE, 'n')
    file['game_map'] = self.state.game_map.game_map
    file['inventory'] = self.state.player_inventory.inventory
    file['game_messages'] = self.state.status_panel.game_messages
    file['objects'] = self.state.objects
    file['player_index'] = self.state.objects.index(self.state.player)
    file['stairs'] = self.state.stairs
    file['dungeon_level'] = self.state.dungeon_level
    file['turn'] = self.state.turn
    file['score'] = self.state.score
    file.close()

  def load_game(self):
    self.state.game_map = Map(self.state)
    self.state.player_inventory = Inventory(self.state)
    file = shelve.open(Constants.SAVE_FILE, 'r')
    self.state.game_map.game_map = file['game_map']
    self.state.player_inventory.inventory = file['inventory']
    self.state.status_panel.game_messages = file['game_messages']
    self.state.objects = file['objects']
    self.state.player = self.state.objects[file['player_index']]
    self.state.stairs = file['stairs']
    self.state.dungeon_level = file['dungeon_level']
    self.state.turn = file['turn']
    self.state.score = file['score']
    file.close()
    self.state.player_spell_inventory = SpellInventory(self.state)
    self.initialize_fov(self.state.dungeon_level)
