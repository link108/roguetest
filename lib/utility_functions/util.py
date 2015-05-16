from lib.random_libs import libtcodpy as libtcod

__author__ = 'cmotevasselani'

from lib.constants.map_constants import MapConstants
from lib.consoles.menu import Menu
from lib.constants.constants import Constants


class Util:

  @staticmethod
  def player_move_or_attack(state, dx, dy):
    x = state.player.x + dx
    y = state.player.y + dy
    target = None
    for object in state.objects:
      if object.fighter and object.x == x and object.y == y:
        target = object
        break
    if target is not None:
      state.player.fighter.attack(target, state)
    else:
      state.player.move(state.objects, state.game_map, dx, dy)
      state.fov_recompute = True

  @staticmethod
  def player_target(state, dx, dy):
    state.game_map.get_map()[state.get_target_x()][state.get_target_y()].set_targeted(False)
    x = state.get_target_x() + dx
    y = state.get_target_y() + dy
    state.game_map.get_map()[x][y].set_targeted(True)
    for object in state.objects:
      if object.x == x and object.y == y:
        state.status_panel.message('You see a : ' + object.name)
        break
    state.set_target(x, y)
    state.set_game_state(Constants.TARGETING)

  @staticmethod
  def get_info(state, object):
    Menu().display_menu_return_index(
      object.get_info(state),
      [], MapConstants.INFO_SCREEN_WIDTH, state.con)
    state.set_player_action(Constants.NOT_VALID_KEY)

  @staticmethod
  def show_character_screen(state, level_up_xp):
    Menu().display_menu_return_index(
        'Character Information\n\nRace: ' + str(state.player_race) + '\nClass: ' + str(state.player_class) +
        '\nLevel: ' + str(state.player.level) + '\nExperience: ' + str(state.player.fighter.xp) +
        '\nExperience to level up: ' + str(level_up_xp) + '\n\nMaximum HP: ' + str(state.player.fighter.max_hp(state)) +
        '\nAttack: ' + str(state.player.fighter.power(state)) + '\nDefense: ' + str(state.player.fighter.defense(state)),
        [], MapConstants.CHARACTER_SCREEN_WIDTH, state.con)
    state.set_player_action(Constants.NOT_VALID_KEY)

  @staticmethod
  def random_choice(chances_dict):
    chances = chances_dict.values()
    strings = chances_dict.keys()
    return strings[Util.random_chance_index(chances)]

  @staticmethod
  def random_chance_index(chances):
    dice = libtcod.random_get_int(0, 1, sum(chances))
    running_sum = 0
    choice = 0
    for w in chances:
      running_sum += w
      if dice <= running_sum:
        return choice
      choice += 1

  @staticmethod
  def closest_monster(state, max_range):
    closest_enemy = None
    closest_dist = max_range + 1
    for object in state.objects:
      if object.fighter and not object == state.player and libtcod.map_is_in_fov(state.fov_map, object.x, object.y):
        dist = state.player.distance_to(object)
        if dist < closest_dist:
          closest_enemy = object
          closest_dist = dist
    return closest_enemy

  @staticmethod
  def check_level_up(state):
    level_up_xp = Constants.LEVEL_UP_BASE + state.player.level + Constants.LEVEL_UP_FACTOR
    if state.player.fighter.xp >= level_up_xp:
      state.player.level += 1
      state.player.fighter.xp -= level_up_xp
      state.status_panel.message('You are now level ' + str(state.player.level) + '! You gain some skillz',
                                 libtcod.yellow)
      choice = None
      while choice == None:
        choice = Menu().display_menu_return_index('Level up! Choose a stat to raise:\n',
                                                  ['Constitution (+20 HP, from ' + str(
                                                    state.player.fighter.max_hp(state)) + ')',
                                                   'Strength (+1 attack, from ' + str(
                                                     state.player.fighter.power(state)) + ')',
                                                   'Agility (+1 defense, from ' + str(
                                                     state.player.fighter.defense(state)) + ')'],
                                                  MapConstants.LEVEL_SCREEN_WIDTH, state.con)
      if choice == 0:
        state.player.fighter.base_max_hp += 20
        state.player.fighter.hp += 20
      elif choice == 1:
        state.player.fighter.base_power += 1
      elif choice == 2:
        state.player.fighter.base_defense += 1
    Util.refresh(state)

  @staticmethod
  def from_dungeon_level(state, table):
    for (value, level) in reversed(table):
      if state.dungeon_level >= level:
        return value
    return 0

  @staticmethod
  def get_equipped_in_slot(state, slot):
    for object in state.player_inventory.inventory:
      if object.equipment and object.equipment.slot == slot and object.equipment.is_equipped:
        return object
    return None

  @staticmethod
  def get_all_equiped(state, obj):
    if obj == state.player:
      equipped_list = []
      for item in state.player_inventory.inventory:
        if item.equipment and item.equipment.is_equipped:
          equipped_list.append(item.equipment)
      return equipped_list
    else:
      return []  # other objects dont have an inventory, TODO Add monster inventory

  # Need a better name
  # Returns a string in the form xy with a single 0 padding
  @staticmethod
  def get_padded_coords(x, y):
    return "{0}{1}".format(str(x).zfill(3), str(y).zfill(3))

  @staticmethod
  def get_coords_from_padded_coords(padded_coords):
    x = padded_coords[:len(padded_coords) / 2]
    y = padded_coords[len(padded_coords) / 2:]
    return int(x), int(y)

  @staticmethod
  def refresh(state):
    state.fov_recompute = True
    Util.render_all(state)
    libtcod.console_flush()
    for object in state.objects:
      object.clear(state.con)

  @staticmethod
  def render_all(state):
    if state.fov_recompute:
      # recompute FOV if needed
      state.fov_recompute = False
      libtcod.map_compute_fov(state.fov_map, state.player.x, state.player.y, MapConstants.TORCH_RADIUS,
                              MapConstants.FOV_LIGHT_WALLS, MapConstants.FOV_ALGO)
      for y in range(MapConstants.MAP_HEIGHT):
        for x in range(MapConstants.MAP_WIDTH):
          visible = libtcod.map_is_in_fov(state.fov_map, x, y)
          wall = state.game_map.get_map()[x][y].block_sight
          targeted = state.game_map.get_map()[x][y].targeted
          if not visible:
            # if not visible right now, player can only see if explored
            if state.game_map.get_map()[x][y].explored:
              if wall:
                libtcod.console_set_char_background(state.con, x, y, MapConstants.COLOR_DARK_WALL, libtcod.BKGND_SET)
              elif targeted:
                libtcod.console_set_char_background(state.con, x, y, MapConstants.COLOR_TARGETED, libtcod.BKGND_SET)
              else:
                libtcod.console_set_char_background(state.con, x, y, MapConstants.COLOR_DARK_GROUND, libtcod.BKGND_SET)
          else:
            # it is visible
            if wall:
              libtcod.console_set_char_background(state.con, x, y, MapConstants.COLOR_LIGHT_WALL, libtcod.BKGND_SET)
            elif targeted:
              libtcod.console_set_char_background(state.con, x, y, MapConstants.COLOR_TARGETED, libtcod.BKGND_SET)
            else:
              libtcod.console_set_char_background(state.con, x, y, MapConstants.COLOR_lIGHT_GROUND, libtcod.BKGND_SET)
            state.game_map.get_map()[x][y].explored = True
    # draw all objects in the list
    for object in state.objects:
      if object != state.player:
        object.draw(state)
    state.player.draw(state)
    libtcod.console_blit(state.con, 0, 0, MapConstants.SCREEN_WIDTH, MapConstants.SCREEN_HEIGHT, 0, 0, 0)
    # prepare to render the GUI panel
    libtcod.console_set_default_background(state.status_panel.get_panel(), libtcod.black)
    libtcod.console_clear(state.status_panel.get_panel())
    # print the game messages, one line at a time
    y = 1
    for (line, color) in state.status_panel.game_messages:
      libtcod.console_set_default_foreground(state.status_panel.get_panel(), color)
      libtcod.console_print_ex(state.status_panel.get_panel(), MapConstants.MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT,
        line)
      y += 1
    # show the player's stats
    state.status_panel.render_bar(1, 1, MapConstants.BAR_WIDTH, 'HP', state.player.fighter.hp,
                                  state.player.fighter.max_hp(state),
                                  libtcod.light_red, libtcod.darker_red)
    state.status_panel.render_bar(1, 2, MapConstants.BAR_WIDTH, 'MP', state.player.caster.mp,
                                  state.player.caster.max_mp(state),
                                  libtcod.light_blue, libtcod.darker_blue)
    libtcod.console_print_ex(state.status_panel.get_panel(), 1, 5, libtcod.BKGND_NONE, libtcod.LEFT,
      'Player level: ' + str(state.player.level))
    libtcod.console_print_ex(state.status_panel.get_panel(), 1, 6, libtcod.BKGND_NONE, libtcod.LEFT,
      'Dungeon level: ' + str(state.dungeon_level))
    libtcod.console_print_ex(state.status_panel.get_panel(), 1, 7, libtcod.BKGND_NONE, libtcod.LEFT,
      'Game State: ' + str(state.get_game_state()))
    libtcod.console_print_ex(state.status_panel.get_panel(), 1, 8, libtcod.BKGND_NONE, libtcod.LEFT,
      'Player Action: ' + str(state.get_player_action()))
    libtcod.console_print_ex(state.status_panel.get_panel(), 1, 9, libtcod.BKGND_NONE, libtcod.LEFT,
      'Score: ' + str(state.score))
    # blit the contents of "panel" to the root console
    libtcod.console_blit(state.status_panel.get_panel(), 0, 0, MapConstants.SCREEN_WIDTH, MapConstants.PANEL_HEIGHT, 0,
      0, MapConstants.PANEL_Y)

