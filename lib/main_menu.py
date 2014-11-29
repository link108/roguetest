
__author__ = 'cmotevasselani'

from lib.random_libs import libtcodpy as libtcod
import shelve

from lib.utility_functions.object import Object
from lib.characters.fighter import Fighter
from lib.map_components.map import Map
from lib.utility_functions.state import State
from lib.items.inventory import Inventory
from lib.items.equipment import Equipment
from lib.constants.map_constants import MapConstants
from lib.constants.constants import Constants
from lib.utility_functions.util import Util
from lib.consoles.menu import Menu

def player_death(state):
    #the game ended, yasd?
    # global game_state
    state.status_panel.message('You died!', libtcod.white)
    Util.set_game_state(Constants.DEAD)
    #player is a corpse
    state.player.char = '%'
    state.player.color = libtcod.dark_red

class MainMenu:

    def __init__(self):
        self.state = State()
        self.menu = Menu()

    def main_menu(self):
        # img = libtcod.image_load('rl_image.png')
        #show the background image, at twice the regular console resolution
        while not libtcod.console_is_window_closed():
            # libtcod.image_blit_2x(img, 0, 0, 0)

            choice = self.menu.display_menu('', ['Play a new game', 'Continue last game', 'Quit'], 24, self.state.con)
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
                break

    def message_box(self, message, size = 50):
        self.menu.display_menu(message, [], size, self.state.con)

    def new_game(self):
        #a warm welcoming message!
        self.state.status_panel.game_messages = []
        self.state.status_panel.message('Welcome stranger! Prepare to perish in the Tombs of the Ancient Kings.', libtcod.red)
        #create the player object

        fighter_component = Fighter(self.state, hp=100, defense=1, power=4, xp=0, death_function=player_death)
        self.state.player = Object(0, 0, '@', 'player', libtcod.white, blocks=True, fighter=fighter_component)
        self.state.player.level = 1
        #the list of all objects
        self.state.objects = [self.state.player]
        self.state.player_inventory = Inventory(self.state)
        self.state.dungeon_level = 1

        equipment_component = Equipment(self.state, slot=Constants.RIGHT_HAND, power_bonus=2)
        obj = Object(0, 0, '-', MapConstants.DAGGER, libtcod.red, equipment=equipment_component, always_visible=True)
        self.state.player_inventory.inventory.append(obj)
        equipment_component.equip()

        self.state.game_map = Map(self.state)
        self.state.game_map.make_map(self.state)
        self.initialize_fov()
        Util.set_player_action(None)

    def initialize_fov(self):
        self.state.fov_map = libtcod.map_new(MapConstants.MAP_WIDTH, MapConstants.MAP_HEIGHT)
        libtcod.console_clear(self.state.con)
        for y in range(MapConstants.MAP_HEIGHT):
            for x in range(MapConstants.MAP_WIDTH):
                libtcod.map_set_properties(self.state.fov_map, x, y, not self.state.game_map.is_blocked_sight(self.state.objects, x, y),
                                           not self.state.game_map.is_blocked_sight(self.state.objects, x, y))

    def play_game(self):
        Util.set_game_state(Constants.PLAYING)
        Util.set_player_action(None)
        self.state.fov_recompute = True

        ###########################################
        #main loop
        ###########################################
        while not libtcod.console_is_window_closed():

            Util.render_all(self.state)
            libtcod.console_flush()
            Util.check_level_up(self.state)

            #erase all objects at their old locations, before they move
            for object in self.state.objects:
                object.clear(self.state.con)

            #handle keys and exit game
            Util.handle_keys(self.state)
            if Util.get_player_action() == Constants.EXIT or self.state.player.color == libtcod.dark_red:
                self.save_game()
                break

            #let monsters take their turn
            if Util.get_game_state() == Constants.PLAYING and Util.get_player_action() != Constants.DID_NOT_TAKE_TURN:
                for object in self.state.objects:
                    if object.ai:
                        object.ai.take_turn(self.state)
            if Util.get_player_action() == Constants.NEXT_LEVEL:
                self.next_level()

    def next_level(self):
        self.state.dungeon_level += 1
        self.state.objects = [self.state.player]
        self.state.status_panel.message('You take a moment to rest and recover 50% health', libtcod.violet)
        self.state.player.fighter.heal(self.state.player.fighter.max_hp / 2)
        self.state.status_panel.message('and now you descend into the depths of the dungeon', libtcod.red)
        self.state.game_map.make_map(self.state)
        self.initialize_fov()
        Util.set_player_action(None)
        self.state.fov_recompute = True

    def save_game(self):
        file = shelve.open(Constants.SAVE_FILE, 'n')
        file['game_map'] = self.state.game_map.game_map
        file['inventory'] = self.state.player_inventory.inventory
        file['game_messages'] = self.state.status_panel.game_messages
        file['objects'] = self.state.objects
        file['player_index'] = self.state.objects.index(self.state.player)
        file['stairs'] = self.state.stairs
        file['dungeon_level'] = self.state.dungeon_level
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
        file.close()
        self.initialize_fov()
