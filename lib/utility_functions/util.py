from lib.random_libs import libtcodpy as libtcod

__author__ = 'cmotevasselani'

from lib.constants.map_constants import MapConstants
from lib.consoles.menu import Menu
from lib.constants.constants import Constants


class Util:

    target_x = None
    target_y = None
    player_action = None

    @staticmethod
    def set_player_action(player_action):
        Util.player_action = player_action

    @staticmethod
    def get_player_action():
        return Util.player_action

    @staticmethod
    def set_game_state(game_state):
        Util.game_state = game_state

    @staticmethod
    def get_game_state():
        return Util.game_state

    @staticmethod
    def set_target(x, y):
        Util.target_x = x
        Util.target_y = y

    @staticmethod
    def get_target_x():
        return Util.target_x

    @staticmethod
    def get_target_y():
        return Util.target_y

    @staticmethod
    def player_move_or_attack(state, dx, dy):

        #the coordinates the player is moving to/attacking
        x = state.player.x + dx
        y = state.player.y + dy

        #try to find an attackable target
        target = None
        for object in state.objects:
            if object.fighter and object.x == x and object.y == y:
                target = object
                break

        #attack if target found, move otherwise
        if target is not None:
            state.player.fighter.attack(target, state)
        else:
            state.player.move(state.objects, state.game_map, dx, dy)
            state.fov_recompute = True

    @staticmethod
    def player_target(state, dx, dy):

        #the coordinates the player is moving to/attacking
        state.game_map.get_map()[Util.get_target_x()][Util.get_target_y()].set_targeted(False)
        x = Util.get_target_x() + dx
        y = Util.get_target_y() + dy
        state.game_map.get_map()[x][y].set_targeted(True)

        #try tofind an attackable target
        for object in state.objects:
            if object.x == x and object.y == y:
                state.status_panel.message('You see a : ' + object.name)
                break
        Util.set_target(x, y)
        Util.set_game_state(Constants.TARGETING)

    @staticmethod
    def handle_keys(state):

        key = libtcod.console_wait_for_keypress(True)
        if key.pressed == False:            #to prevent actions from being preformed twice
            Util.set_player_action(Constants.DID_NOT_TAKE_TURN)

        if key.vk == libtcod.KEY_ENTER and key.lalt:        # Toggle fullscreen
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        # elif key.vk == libtcod.KEY_ESCAPE:                  # exit game
        elif key.vk == libtcod.KEY_ESCAPE:
            Util.set_player_action(Constants.EXIT)
            # Util.set_game_state(Util.EXIT)

        game_state = Util.get_game_state()
        if game_state == Constants.PLAYING:
            Util.handle_playing_keys(key, state)
        elif game_state == Constants.TARGETING:
            Util.handle_targeting_keys(key, state)
        elif game_state == Constants.FOUND_TARGET:
            Util.set_game_state(Constants.FOUND_TARGET)

    @staticmethod
    def handle_targeting_keys(key, state):
        #movement keys
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
                Util.set_player_action(Constants.DID_NOT_TAKE_TURN)
        elif key.vk == libtcod.KEY_ESCAPE:
            Util.set_game_state(Constants.PLAYING)
        elif key.vk == libtcod.KEY_ENTER:
            Util.set_game_state(Constants.FOUND_TARGET)
        else:
            Util.set_player_action(Constants.DID_NOT_TAKE_TURN)

    @staticmethod
    def handle_playing_keys(key, state):
        #movement keys
        if key.vk == libtcod.KEY_CHAR:
            if key.c == ord('k'):
                Util.player_move_or_attack(state,  0, -1)
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
            elif key.c == ord('i'):
                chosen_item = state.player_inventory.inventory_menu('Press the key next to an item to use it, or any other to cancel.\n', state)
                if chosen_item is not None:
                    chosen_item.use(state)
            elif key.c == ord('d'):
                chosen_item = state.player_inventory.inventory_menu('Press the key next to an item to drop it, or any other to cancel.\n', state)
                if chosen_item is not None:
                    chosen_item.drop(state)
            elif key.c == ord('g'):
                #pick up an item
                for object in state.objects:  #look for an item in the player's tile
                    if object.x == state.player.x and object.y == state.player.y and object.item:
                        object.item.pick_up(state)
                        break
            elif key.c == ord('>'):
                padded_player_coords = Util.get_padded_coords(state.player.x, state.player.y)
                if padded_player_coords in state.stairs[state.dungeon_level][MapConstants.DOWN_STAIRS_OBJECT].keys():
                    Util.set_player_action(Constants.NEXT_LEVEL)
            elif key.c == ord('<'):
                padded_player_coords = Util.get_padded_coords(state.player.x, state.player.y)
                if padded_player_coords in state.stairs[state.dungeon_level][MapConstants.UP_STAIRS_OBJECT].keys():
                    Util.set_player_action(Constants.PREVIOUS_LEVEL)
            elif key.c == ord('c'):
                #show character information
                level_up_xp = Constants.LEVEL_UP_BASE + state.player.level * Constants.LEVEL_UP_FACTOR
                Menu().display_menu('Character Information\n\nLevel: ' + str(state.player.level) + '\nExperience: ' + str(state.player.fighter.xp) +
                    '\nExperience to level up: ' + str(level_up_xp) + '\n\nMaximum HP: ' + str(state.player.fighter.max_hp) +
                    '\nAttack: ' + str(state.player.fighter.power) + '\nDefense: ' + str(state.player.fighter.defense), [], MapConstants.CHARACTER_SCREEN_WIDTH, state.con)
            else:
                Util.set_player_action(Constants.DID_NOT_TAKE_TURN)

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
    def target_tile(state):
        Util.set_game_state(Constants.TARGETING)
        Util.set_target(state.player.x, state.player.y)

        while Util.get_game_state() == Constants.TARGETING:
            # How to deal with returning either multiple values or single value: ie x, y or gamestate
            Util.handle_keys(state)
            Util.refresh(state)
            # Util.set_game_state(Util.handle_keys(state))

        if Util.get_game_state() == Constants.FOUND_TARGET:
            x, y = Util.get_target_coords()
            Util.set_game_state(Constants.PLAYING)
        # TODO: Make target class? how to save/where to save targeting coords?
        # while
        if Util.get_target_x() is None or Util.get_target_y() is None:
            return Constants.CANCELLED
        state.game_map.get_map()[Util.get_target_x()][Util.get_target_y()].set_targeted(False)
        return Util.get_target_x(), Util.get_target_y()

    @staticmethod
    def refresh(state):
        # Util.render_all(state.game_map, state.fov_map, True, state.status_panel)

        state.fov_recompute = True
        Util.render_all(state)
        libtcod.console_flush()


    @staticmethod
    def closest_monster(state, max_range):
        # Find closest enemy, up to a max range and within the player's FOV
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
    def target_monster(state, max_range=None):
        Util.set_game_state(Constants.TARGETING)
        while Util.get_game_state() == Constants.TARGETING:
            (x, y) = Util.target_tile(state)
            if x is None or y is None:
                return Constants.CANCELLED
            for object in state.objects:
                if object.x == x and object.y == y and object.fighter and object != state.player:
                    return object

    @staticmethod
    def check_level_up(state):
        level_up_xp = Constants.LEVEL_UP_BASE + state.player.level + Constants.LEVEL_UP_FACTOR
        if state.player.fighter.xp >= level_up_xp:
            state.player.level += 1
            state.player.fighter.xp -= level_up_xp
            state.status_panel.message('You are now level ' + str(state.player.level) + '! You gain some skillz', libtcod.yellow)
            choice = None
            while choice == None:
                choice = Menu().display_menu('Level up! Choose a stat to raise:\n',
                    ['Constitution (+20 HP, from ' + str(state.player.fighter.max_hp) + ')',
                    'Strength (+1 attack, from ' + str(state.player.fighter.power) + ')',
                    'Agility (+1 defense, from ' + str(state.player.fighter.defense) + ')'], MapConstants.LEVEL_SCREEN_WIDTH, state.con)
            if choice == 0:
                state.player.fighter.max_hp += 20
                state.player.fighter.hp += 20
            elif choice == 1:
                state.player.fighter.power += 1
            elif choice == 2:
                state.player.fighter.defense += 1
        Util.refresh(state)


    @staticmethod
    def from_dungeon_level(state, table):
        for (value, level) in reversed(table):
            if state.dungeon_level >= level:
                return value
        return 0

    @staticmethod
    def get_target_coords():
        x = Util.get_target_y()
        y = Util.get_target_y()
        return x, y

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
        x = padded_coords[:len(padded_coords)/2]
        y = padded_coords[len(padded_coords)/2:]
        return int(x), int(y)

    @staticmethod
    def render_all(state):
        if state.fov_recompute:
            #recompute FOV if needed
            state.fov_recompute = False
            libtcod.map_compute_fov(state.fov_map, state.player.x, state.player.y, MapConstants.TORCH_RADIUS, MapConstants.FOV_LIGHT_WALLS, MapConstants.FOV_ALGO)
            for y in range(MapConstants.MAP_HEIGHT):
                for x in range(MapConstants.MAP_WIDTH):
                    visible = libtcod.map_is_in_fov(state.fov_map, x, y)
                    wall = state.game_map.get_map()[x][y].block_sight
                    targeted = state.game_map.get_map()[x][y].targeted
                    if not visible:
                        #if not visible right now, player can only see if explored
                        if state.game_map.get_map()[x][y].explored:
                            if wall:
                                libtcod.console_set_char_background(state.con, x, y, MapConstants.COLOR_DARK_WALL, libtcod.BKGND_SET)
                            elif targeted:
                                libtcod.console_set_char_background(state.con, x, y,  MapConstants.COLOR_TARGETED, libtcod.BKGND_SET)
                            else:
                                libtcod.console_set_char_background(state.con, x, y, MapConstants.COLOR_DARK_GROUND, libtcod.BKGND_SET)
                    else:
                        #it is visible
                        if wall:
                            libtcod.console_set_char_background(state.con, x, y, MapConstants.COLOR_LIGHT_WALL, libtcod.BKGND_SET)
                        elif targeted:
                            libtcod.console_set_char_background(state.con, x, y, MapConstants.COLOR_TARGETED, libtcod.BKGND_SET)
                        else:
                            libtcod.console_set_char_background(state.con, x, y, MapConstants.COLOR_lIGHT_GROUND, libtcod.BKGND_SET)
                        state.game_map.get_map()[x][y].explored = True
        #draw all objects in the list
        for object in state.objects:
            if object != state.player:
                object.draw(state)
        state.player.draw(state)
        libtcod.console_blit(state.con, 0, 0, MapConstants.SCREEN_WIDTH, MapConstants.SCREEN_HEIGHT, 0, 0, 0)
        #prepare to render the GUI panel
        libtcod.console_set_default_background(state.status_panel.get_panel(), libtcod.black)
        libtcod.console_clear(state.status_panel.get_panel())
        #print the game messages, one line at a time
        y = 1
        for (line, color) in state.status_panel.game_messages:
            libtcod.console_set_default_foreground(state.status_panel.get_panel(), color)
            libtcod.console_print_ex(state.status_panel.get_panel(), MapConstants.MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
            y += 1
        #show the player's stats
        state.status_panel.render_bar(1, 1, MapConstants.BAR_WIDTH, 'HP', state.player.fighter.hp, state.player.fighter.max_hp,
            libtcod.light_red, libtcod.darker_red)
        libtcod.console_print_ex(state.status_panel.get_panel(), 1, 3, libtcod.BKGND_NONE, libtcod.LEFT, 'Player level: ' + str(state.player.level))
        libtcod.console_print_ex(state.status_panel.get_panel(), 1, 4, libtcod.BKGND_NONE, libtcod.LEFT, 'Dungeon level: ' + str(state.dungeon_level))
        libtcod.console_print_ex(state.status_panel.get_panel(), 1, 6, libtcod.BKGND_NONE, libtcod.LEFT, 'Game State: ' + str(Util.get_game_state()))
        #blit the contents of "panel" to the root console
        libtcod.console_blit(state.status_panel.get_panel(), 0, 0, MapConstants.SCREEN_WIDTH, MapConstants.PANEL_HEIGHT, 0, 0, MapConstants.PANEL_Y)
        #show the player's stats
        # libtcod.console_set_default_foreground(con, libtcod.white)
        # libtcod.console_print_ex(0, 1, SCREEN_HEIGHT - 2, libtcod.BKGND_NONE, libtcod.LEFT,
        #         'HP: ' + str(player.fighter.hp) + '/' + str(player.fighter.max_hp))

