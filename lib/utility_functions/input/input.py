__author__ = 'cmotevasselani'

from lib.random_libs import libtcodpy as libtcod
from lib.constants.constants import Constants
from lib.utility_functions.util import Util
from lib.consoles.menu import Menu
from lib.constants.map_constants import MapConstants


class Input:


  @staticmethod
  def wait_for_keypress(state):
    key = libtcod.console_wait_for_keypress(True)
    if key.pressed == False:  # to prevent actions from being preformed twice
      state.set_player_action(Constants.DID_NOT_TAKE_TURN)
    return key

  @staticmethod
  def handle_keys(state):
    key = Input.wait_for_keypress(state)
    while key.vk == libtcod.KEY_SHIFT:
      key = Input.wait_for_keypress(state)

    if key.vk == libtcod.KEY_ENTER and key.lalt:  # Toggle fullscreen
      libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    elif key.vk == libtcod.KEY_ESCAPE:
      state.set_player_action(Constants.EXIT)

    game_state = state.get_game_state()
    if game_state == Constants.PLAYING:
      Input.handle_playing_keys(key, state)
    elif game_state == Constants.TARGETING:
      Input.handle_targeting_keys(key, state)
    elif game_state == Constants.FOUND_TARGET:
      state.set_game_state(Constants.FOUND_TARGET)

    if state.get_player_action() == Constants.DID_NOT_TAKE_TURN:
      state.set_player_action(None)
    elif state.get_player_action() == Constants.NOT_VALID_KEY:
      state.set_player_action(Constants.DID_NOT_TAKE_TURN)

  @staticmethod
  def handle_targeting_keys(key, state):
    if key.vk == libtcod.KEY_CHAR:
      if key.c == ord('k'):
        return Util.player_target(state, 0, -1)
      elif key.c == ord('j'):
        return Util.player_target(state, 0, 1)
      elif key.c == ord('h'):
        return Util.player_target(state, -1, 0)
      elif key.c == ord('l'):
        return Util.player_target(state, 1, 0)
      elif key.c == ord('y'):
        return Util.player_target(state, -1, -1)
      elif key.c == ord('u'):
        return Util.player_target(state, 1, -1)
      elif key.c == ord('b'):
        return Util.player_target(state, -1, 1)
      elif key.c == ord('n'):
        return Util.player_target(state, 1, 1)
      else:
        state.set_player_action(Constants.NOT_VALID_KEY)
    elif key.vk == libtcod.KEY_ESCAPE:
      state.set_game_state(Constants.PLAYING)
    elif key.vk == libtcod.KEY_ENTER:
      state.set_game_state(Constants.FOUND_TARGET)
    else:
      state.set_player_action(Constants.NOT_VALID_KEY)

  @staticmethod
  def handle_playing_keys(key, state):
    if key.vk == libtcod.KEY_CHAR:
      if key.c == ord('k'):
        Util.player_move_or_attack(state, 0, -1)
      elif key.c == ord('j'):
        Util.player_move_or_attack(state, 0, 1)
      elif key.c == ord('h'):
        Util.player_move_or_attack(state, -1, 0)
      elif key.c == ord('l'):
        Util.player_move_or_attack(state, 1, 0)
      elif key.c == ord('y'):
        Util.player_move_or_attack(state, -1, -1)
      elif key.c == ord('u'):
        Util.player_move_or_attack(state, 1, -1)
      elif key.c == ord('b'):
        Util.player_move_or_attack(state, -1, 1)
      elif key.c == ord('n'):
        Util.player_move_or_attack(state, 1, 1)
      elif key.c == ord('.'):
        pass
      elif key.c == ord('v'):
        Util.look(state)
        state.set_player_action(Constants.NOT_VALID_KEY)
      elif key.c == ord('i'):
        chosen_item = state.player_inventory.inventory_menu(
          'Press the key next to an item to use it, or any other to cancel.\n', state)
        if chosen_item is not None:
          chosen_item.use(state)
          # else:
          #     state.set_player_action(Constants.NOT_VALID_KEY)
      elif key.c == ord('I'):
        chosen_spell = state.player_spell_inventory.spell_menu(
          'Press the key next to a spell to use it, or any other to cancel.\n', state)
        if chosen_spell is not None:
          chosen_spell.cast(state, state.player)
      elif key.c == ord('d'):
        chosen_item = state.player_inventory.inventory_menu(
          'Press the key next to an item to drop it, or any other to cancel.\n', state)
        if chosen_item is not None:
          chosen_item.drop(state)
      elif key.c == ord('g'):
        # pick up an item
        for object in state.objects:  # look for an item in the player's tile
          if object.x == state.player.x and object.y == state.player.y and object.item:
            object.item.pick_up(state)
            break
      elif key.c == ord('>'):
        padded_player_coords = Util.get_padded_coords(state.player.x, state.player.y)
        if padded_player_coords in state.stairs[state.dungeon_level][MapConstants.DOWN_STAIRS_OBJECT].keys():
          state.set_player_action(Constants.NEXT_LEVEL)
      elif key.c == ord('<'):
        padded_player_coords = Util.get_padded_coords(state.player.x, state.player.y)
        if padded_player_coords in state.stairs[state.dungeon_level][MapConstants.UP_STAIRS_OBJECT].keys():
          state.set_player_action(Constants.PREVIOUS_LEVEL)
      elif key.c == ord('c'):
        # show character information
        level_up_xp = Constants.LEVEL_UP_BASE + state.player.level * Constants.LEVEL_UP_FACTOR
        Util.show_character_screen(state, level_up_xp)
        Util.refresh(state)
      else:
        state.set_player_action(Constants.NOT_VALID_KEY)

  @staticmethod
  def get_info(state, object):
    Menu().display_menu_return_index(
      object.get_info(state),
      [], MapConstants.INFO_SCREEN_WIDTH, state.con)
    state.set_player_action(Constants.NOT_VALID_KEY)

  @staticmethod
  def look(state):
    state.set_game_state(Constants.TARGETING)
    x, y = state.player.x, state.player.y
    while state.get_game_state() == Constants.TARGETING:
      (x, y) = Util.target_tile(state, x, y)
      if x is None or y is None:
        return Constants.CANCELLED
      for object in state.objects:
        if object.x == x and object.y == y:
          state.get_info(state, object)
          state.set_game_state(Constants.TARGETING)
          state.set_target(x, y)

  @staticmethod
  def target_tile(state, start_x=None, start_y=None):
    state.set_game_state(Constants.TARGETING)
    if start_x is None or start_y is None:
      state.set_target(state.player.x, state.player.y)
    else:
      state.set_target(start_x, start_y)
    while state.get_game_state() == Constants.TARGETING:
      Input.handle_keys(state)
      Util.refresh(state)

    if state.get_game_state() == Constants.FOUND_TARGET:
      x, y = state.get_target_coords()
      state.set_game_state(Constants.PLAYING)
    # TODO: Make target class? how to save/where to save targeting coords?
    # while
    if state.get_target_x() is None or state.get_target_y() is None:
      return Constants.CANCELLED
    state.game_map.get_map()[state.get_target_x()][state.get_target_y()].set_targeted(False)
    return state.get_target_x(), state.get_target_y()

  @staticmethod
  def target_monster(state, max_range=None):
    state.set_game_state(Constants.TARGETING)
    while state.get_game_state() == Constants.TARGETING:
      (x, y) = Input.target_tile(state)
      if x is None or y is None:
        return Constants.CANCELLED
      for object in state.objects:
        if object.x == x and object.y == y and object.fighter and object != state.player:
          return object






