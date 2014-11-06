from lib import libtcodpy as libtcod
from lib.item import Item

__author__ = 'cmotevasselani'

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
BAR_WIDTH = 20
MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1
# LIMIT_FPS = 20

MAP_WIDTH = 80
MAP_HEIGHT = 43
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

FOV_ALGO = 0    #default FOV algorithm
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10
MAX_ROOM_MONSTERS = 3

color_targeted = libtcod.green
color_dark_wall = libtcod.Color(0, 0, 100)
color_light_wall = libtcod.Color(130, 110, 50)
color_dark_ground = libtcod.Color(50, 50, 150)
color_light_ground = libtcod.Color(200, 180, 50)

class Util:

    TARGETING = 'targeting'
    FOUND_TARGET = 'found-target'
    PLAYING = 'playing'
    EXIT = 'exit'
    DEAD = 'dead'
    DID_NOT_TAKE_TURN = 'did-not-take-turn'

    def __init__(self):
        self.con = None
        self.SCREEN_WIDTH = None
        self.SCREEN_HEIGHT = None
        self.status_panel = None
        self.player = None
        self.fov_map = None
        self.objects = None
        self.player_inventory = None
        self.game_map = None
        self.target_x = None
        self.target_y = None
        self.player_action = None

    def set_attr(self, player, status_panel, fov_map, objects, inventory, game_map, con, screen_width, screen_height):
        self.player = player
        self.status_panel = status_panel
        self.fov_map = fov_map
        self.objects = objects
        self.player_inventory = inventory
        self.game_map = game_map
        self.con = con
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.target_x = None
        self.target_y = None
        self.player_action = None

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
    def player_move_or_attack(util, dx, dy):
        global fov_recompute

        #the coordinates the player is moving to/attacking
        x = util.player.x + dx
        y = util.player.y + dy

        #try to find an attackable target
        target = None
        for object in util.objects:
            if object.fighter and object.x == x and object.y == y:
                target = object
                break

        #attack if target found, move otherwise
        if target is not None:
            util.player.fighter.attack(target, util.objects, util.status_panel)
        else:
            util.player.move(util.objects, util.game_map, dx, dy)
            fov_recompute = True

    @staticmethod
    def player_target(util, dx, dy):

        #the coordinates the player is moving to/attacking
        util.game_map.get_map()[Util.get_target_x()][Util.get_target_y()].set_targeted(False)
        x = Util.get_target_x() + dx
        y = Util.get_target_y() + dy
        util.game_map.get_map()[x][y].set_targeted(True)

        #try tofind an attackable target
        for object in util.objects:
            if object.x == x and object.y == y:
                util.status_panel.message('You see a : ' + object.name)
                break
        Util.set_target(x, y)
        Util.set_game_state(Util.TARGETING)

    @staticmethod
    def handle_keys(util):
        global fov_recompute

        #key = libtcod.console_check_for_keypress()    #real-time
        key = libtcod.console_wait_for_keypress(True)
        if key.pressed == False:            #to prevent actions from being preformed twice
            Util.set_player_action(Util.DID_NOT_TAKE_TURN)

        if key.vk == libtcod.KEY_ENTER and key.lalt:        # Toggle fullscreen
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        # elif key.vk == libtcod.KEY_ESCAPE:                  # exit game
        elif key.vk == libtcod.KEY_ESCAPE and key.lalt:                  # exit game
            Util.set_player_action(Util.EXIT)

        game_state = Util.get_game_state()
        if game_state == Util.PLAYING:
            Util.handle_playing_keys(key, util)
        elif game_state == Util.TARGETING:
            Util.handle_targeting_keys(key, util)
        elif game_state == Util.FOUND_TARGET:
            Util.set_game_state(Util.FOUND_TARGET)

    @staticmethod
    def handle_targeting_keys(key, util):
        #movement keys
        if key.vk == libtcod.KEY_CHAR:
            if key.c == ord('k'):
                return Util.player_target(util, 0, -1)
            elif key.c == ord('j'):
                return Util.player_target(util, 0, 1)
            elif key.c == ord('h'):
                return Util.player_target(util, -1, 0)
            elif key.c == ord('l'):
                return Util.player_target(util, 1, 0)
            elif key.c == ord('y'):
                return Util.player_target(util, -1, -1)
            elif key.c == ord('u'):
                return Util.player_target(util, 1, -1)
            elif key.c == ord('b'):
                return Util.player_target(util, -1, 1)
            elif key.c == ord('n'):
                return Util.player_target(util, 1, 1)
            else:
                Util.set_player_action(Util.DID_NOT_TAKE_TURN)
        elif key.vk == libtcod.KEY_ESCAPE:
            Util.set_game_state(Util.PLAYING)
        elif key.vk == libtcod.KEY_ENTER:
            Util.set_game_state(Util.FOUND_TARGET)
        else:
            Util.set_player_action(Util.DID_NOT_TAKE_TURN)

    @staticmethod
    def handle_playing_keys(key, util):
        #movement keys
        if key.vk == libtcod.KEY_CHAR:
            if key.c == ord('k'):
                Util.player_move_or_attack(util,  0, -1)
            elif key.c == ord('j'):
                Util.player_move_or_attack(util, 0, 1)
            elif key.c == ord('h'):
                Util.player_move_or_attack(util, -1, 0)
            elif key.c == ord('l'):
                Util.player_move_or_attack(util, 1, 0)
            elif key.c == ord('y'):
                Util.player_move_or_attack(util, -1, -1)
            elif key.c == ord('u'):
                Util.player_move_or_attack(util, 1, -1)
            elif key.c == ord('b'):
                Util.player_move_or_attack(util, -1, 1)
            elif key.c == ord('n'):
                Util.player_move_or_attack(util, 1, 1)
            elif key.c == ord('i'):
                chosen_item = util.player_inventory.inventory_menu('Press the key next to an item to use it, or any other to cancel.\n', util.con, util.SCREEN_WIDTH, util.SCREEN_HEIGHT)
                if chosen_item is not None:
                    chosen_item.use(util)
            elif key.c == ord('g'):
                #pick up an item
                for object in util.objects:  #look for an item in the player's tile
                    if object.x == util.player.x and object.y == util.player.y and object.item:
                        object.item.pick_up(util.player_inventory)
                        break
            else:
                Util.set_player_action(Util.DID_NOT_TAKE_TURN)

    @staticmethod
    def player_death(player, objects, status_panel):
        #the game ended, yasd?
        # global game_state
        status_panel.message('You died!', libtcod.white)
        Util.set_game_state(Util.DEAD)
        #player is a corpse
        player.char = '%'
        player.color = libtcod.dark_red

    @staticmethod
    def target_tile(util):
        Util.set_game_state(Util.TARGETING)
        Util.set_target(util.player.x, util.player.y)

        while Util.get_game_state() == Util.TARGETING:
            # How to deal with returning either multiple values or single value: ie x, y or gamestate
            Util.handle_keys(util)
            Util.refresh(util)
            # Util.set_game_state(Util.handle_keys(util))

        if Util.get_game_state() == Util.FOUND_TARGET:
            x, y = Util.get_target_coords(util)
            Util.set_game_state(Util.PLAYING)
        # TODO: Make target class? how to save/where to save targeting coords?
        # while
        if Util.get_target_x() is None or Util.get_target_y() is None:
            return Item.CANCELLED
        return Util.get_target_x(), Util.get_target_y()

    @staticmethod
    def refresh(util):
        # Util.render_all(util.game_map, util.fov_map, True, util.status_panel)
        Util.render_all(util, True)
        libtcod.console_flush()


    @staticmethod
    def get_target_coords(util):
        x = util.get_target_y()
        y = util.get_target_y()
        return x, y

    @staticmethod
    def monster_death(monster, objects, status_panel):
        #monster turns into a corpse, does not block, cant be attacked, does not move
        status_panel.message(monster.name.capitalize() + ' is dead!', libtcod.white)
        monster.char = '%'
        monster.color = libtcod.dark_red
        monster.blocks = False
        monster.fighter = None
        monster.ai = None
        monster.name = 'remains of ' + monster.name
        monster.send_to_back(objects)



    @staticmethod
    def render_all(util, fov_recompute):
        global color_dark_wall, color_light_wall
        global color_dark_ground, color_light_ground

        if fov_recompute:
            #recompute FOV if needed
            fov_recompute = False
            libtcod.map_compute_fov(util.fov_map, util.player.x, util.player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
            for y in range(MAP_HEIGHT):
                for x in range(MAP_WIDTH):
                    visible = libtcod.map_is_in_fov(util.fov_map, x, y)
                    wall = util.game_map.get_map()[x][y].block_sight
                    targeted = util.game_map.get_map()[x][y].targeted
                    if not visible:
                        #if not visible right now, player can only see if explored
                        if util.game_map.get_map()[x][y].explored:
                            if wall:
                                libtcod.console_set_char_background(util.con, x, y, color_dark_wall, libtcod.BKGND_SET)
                            elif targeted:
                                libtcod.console_set_char_background(util.con, x, y, color_targeted, libtcod.BKGND_SET)
                            else:
                                libtcod.console_set_char_background(util.con, x, y, color_dark_ground, libtcod.BKGND_SET)
                    else:
                        #it is visible
                        if wall:
                            libtcod.console_set_char_background(util.con, x, y, color_light_wall, libtcod.BKGND_SET)
                        elif targeted:
                            libtcod.console_set_char_background(util.con, x, y, color_targeted, libtcod.BKGND_SET)
                        else:
                            libtcod.console_set_char_background(util.con, x, y, color_light_ground, libtcod.BKGND_SET)
                        util.game_map.get_map()[x][y].explored = True

        #draw all objects in the list
        for object in util.objects:
            if object != util.player:
                object.draw(util.fov_map, util.con)
        util.player.draw(util.fov_map, util.con)

        libtcod.console_blit(util.con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

        #prepare to render the GUI panel
        libtcod.console_set_default_background(util.status_panel.get_panel(), libtcod.black)
        libtcod.console_clear(util.status_panel.get_panel())

        #print the game messages, one line at a time
        y = 1
        for (line, color) in util.status_panel.game_messages:
            libtcod.console_set_default_foreground(util.status_panel.get_panel(), color)
            libtcod.console_print_ex(util.status_panel.get_panel(), MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
            y += 1
        #show the player's stats
        util.status_panel.render_bar(1, 1, BAR_WIDTH, 'HP', util.player.fighter.hp, util.player.fighter.max_hp,
            libtcod.light_red, libtcod.darker_red)

        #blit the contents of "panel" to the root console
        libtcod.console_blit(util.status_panel.get_panel(), 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)

        #show the player's stats
        # libtcod.console_set_default_foreground(con, libtcod.white)
        # libtcod.console_print_ex(0, 1, SCREEN_HEIGHT - 2, libtcod.BKGND_NONE, libtcod.LEFT,
        #         'HP: ' + str(player.fighter.hp) + '/' + str(player.fighter.max_hp))

