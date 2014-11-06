from lib import libtcodpy as libtcod
from lib.item import Item

__author__ = 'cmotevasselani'


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
    def player_move_or_attack(player, objects, game_map, dx, dy, status_panel):
        global fov_recompute

        #the coordinates the player is moving to/attacking
        x = player.x + dx
        y = player.y + dy

        #try to find an attackable target
        target = None
        for object in objects:
            if object.fighter and object.x == x and object.y == y:
                target = object
                break

        #attack if target found, move otherwise
        if target is not None:
            player.fighter.attack(target, objects, status_panel)
        else:
            player.move(objects, game_map, dx, dy)
            fov_recompute = True

    @staticmethod
    def player_target(player, objects, game_map, dx, dy, status_panel):

        #the coordinates the player is moving to/attacking
        x = Util.get_target_x() + dx
        y = Util.get_target_y() + dy

        #try tofind an attackable target
        for object in objects:
            if object.x == x and object.y == y:
                status_panel.message('You see a : ' + object.name)
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

        {
            Util.PLAYING : Util.handle_playing_keys(key, util),
            Util.TARGETING : Util.handle_targeting_keys(key, util),
            Util.FOUND_TARGET : Util.set_game_state(Util.FOUND_TARGET)
        }[Util.get_game_state()]

        # if Util.get_game_state() == Util.PLAYING:
        #     Util.handle_playing_keys(key, util)
        # elif Util.get_game_state() == Util.TARGETING:
        #     Util.handle_targeting_keys(key, util)
        # elif util.game_state == Util.FOUND_TARGET:
        #     Util.set_game_state(Util.FOUND_TARGET)


    @staticmethod
    def handle_targeting_keys(key, util):
        #movement keys
        if key.vk == libtcod.KEY_CHAR:
            if key.c == ord('k'):
                return Util.player_target(util.player, util.objects, util.game_map,  0, -1, util.status_panel)
            elif key.c == ord('j'):
                return Util.player_target(util.player, util.objects, util.game_map, 0, 1, util.status_panel)
            elif key.c == ord('h'):
                return Util.player_target(util.player, util.objects, util.game_map, -1, 0, util.status_panel)
            elif key.c == ord('l'):
                return Util.player_target(util.player, util.objects, util.game_map, 1, 0, util.status_panel)
            elif key.c == ord('y'):
                return Util.player_target(util.player, util.objects, util.game_map, -1, -1, util.status_panel)
            elif key.c == ord('u'):
                return Util.player_target(util.player, util.objects, util.game_map, 1, -1, util.status_panel)
            elif key.c == ord('b'):
                # return Util.player_target(util.player, util.objects, util.game_map, -1, 1, util.status_panel)
                blah = Util.player_target(util.player, util.objects, util.game_map, -1, 1, util.status_panel)
                return blah
            elif key.c == libtcod.KEY_ESCAPE:
                Util.get_game_state(Util.PLAYING)
            elif key.c == libtcod.KEY_ENTER:
                Util.get_game_state(Util.FOUND_TARGET)
                #pick up an item
            else:
                Util.set_player_action(Util.DID_NOT_TAKE_TURN)

    @staticmethod
    def handle_playing_keys(key, util):
        #movement keys
        if key.vk == libtcod.KEY_CHAR:
            if key.c == ord('k'):
                Util.player_move_or_attack(util.player, util.objects, util.game_map,  0, -1, util.status_panel)
            elif key.c == ord('j'):
                Util.player_move_or_attack(util.player, util.objects, util.game_map, 0, 1, util.status_panel)
            elif key.c == ord('h'):
                Util.player_move_or_attack(util.player, util.objects, util.game_map, -1, 0, util.status_panel)
            elif key.c == ord('l'):
                Util.player_move_or_attack(util.player, util.objects, util.game_map, 1, 0, util.status_panel)
            elif key.c == ord('y'):
                Util.player_move_or_attack(util.player, util.objects, util.game_map, -1, -1, util.status_panel)
            elif key.c == ord('u'):
                Util.player_move_or_attack(util.player, util.objects, util.game_map, 1, -1, util.status_panel)
            elif key.c == ord('b'):
                Util.player_move_or_attack(util.player, util.objects, util.game_map, -1, 1, util.status_panel)
            elif key.c == ord('n'):
                Util.player_move_or_attack(util.player, util.objects, util.game_map, 1, 1, util.status_panel)
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
                return Util.DID_NOT_TAKE_TURN

    @staticmethod
    def player_death(player, objects, status_panel):
        #the game ended, yasd?
        # global game_state
        status_panel.message('You died!', libtcod.white)
        game_state = Util.DEAD
        #player is a corpse
        player.char = '%'
        player.color = libtcod.dark_red

    @staticmethod
    def target_tile(util):
        Util.set_game_state(Util.TARGETING)
        Util.set_target(util.player.x, util.player.y)

        while util.game_state == Util.TARGETING:
            util.status_panel.message('player x: ' + str(util.player.x) + ', player y: ' + str(util.player.y), libtcod.turquoise)
            util.status_panel.message('x: ' + str(Util.get_target_x()) + ', y: ' + str(Util.get_target_y()), libtcod.turquoise)
            # How to deal with returning either multiple values or single value: ie x, y or gamestate
            Util.set_game_state(Util.handle_keys(util))
            util.status_panel.message('util.game_state: ' + Util.get_game_state(), libtcod.turquoise)

        if Util.get_game_state() == Util.FOUND_TARGET:
            x, y = Util.get_target_coords(util)
        # TODO: Make target class? how to save/where to save targeting coords?
        # while
        if Util.get_target_x() is None or Util.get_target_y() is None:
            return Item.CANCELLED
        return Util.get_target_x(), Util.get_target_y()

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
