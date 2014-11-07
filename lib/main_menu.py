__author__ = 'cmotevasselani'

from lib import libtcodpy as libtcod

from lib.object import Object
from lib.fighter import Fighter
from lib.map import Map
from lib.state import State
from lib.inventory import Inventory
from lib.map_constants import MapConstants
from lib.util import Util
from lib.consoles.menu import Menu

class MainMenu:

    def __init__(self):
        self.state = State()
        self.menu = Menu()

    def main_menu(self):
        img = libtcod.image_load('rl_image.png')
        #show the background image, at twice the regular console resolution
        while not libtcod.console_is_window_closed():
            libtcod.image_blit_2x(img, 0, 0, 0)

            choice = self.menu.display_menu('', ['Play a new game', 'Continue last game', 'Quit'], 24, self.state.con)
            if choice == 0:
                self.new_game()
                self.play_game()
            elif choice == 2:
                break

    def new_game(self):
        #a warm welcoming message!
        self.state.status_panel.message('Welcome stranger! Prepare to perish in the Tombs of the Ancient Kings.', libtcod.red)
        self.state.util = Util()

        #create the player object

        # fighter_component = Fighter(hp = 30, defense = 2, power = 5, death_function = Util.player_death)
        fighter_component = Fighter(hp=300, defense=20, power=50, death_function=Util.player_death)
        self.state.player = Object(0, 0, '@', 'player', libtcod.white, blocks=True, fighter=fighter_component)
        #the list of all objects
        self.state.objects = [self.state.player]
        self.state.player_inventory = Inventory(self.state.status_panel, self.state.objects, self.state.player)
        self.state.game_map = Map(self.state.status_panel, self.state.player)
        self.state.game_map.make_map(self.state.objects, self.state.player)
        self.initialize_fov()
        self.state.util.set_attr(self.state.player, self.state.status_panel, self.state.fov_map, self.state.objects, self.state.player_inventory, self.state.game_map, self.state.con)
        Util.set_player_action(None)

    def initialize_fov(self):
        self.state.fov_map = libtcod.map_new(MapConstants.MAP_WIDTH, MapConstants.MAP_HEIGHT)
        libtcod.console_clear(self.state.con)
        for y in range(MapConstants.MAP_HEIGHT):
            for x in range(MapConstants.MAP_WIDTH):
                libtcod.map_set_properties(self.state.fov_map, x, y, not self.state.game_map.is_blocked_sight(self.state.objects, x, y),
                                           not self.state.game_map.is_blocked_sight(self.state.objects, x, y))

    def play_game(self):
        Util.set_game_state(Util.PLAYING)

        ###########################################
        #main loop
        ###########################################
        while not libtcod.console_is_window_closed():

            Util.render_all(self.state.util, self.state.fov_recompute)
            libtcod.console_flush()

            #erase all objects at their old locations, before they move
            for object in self.state.objects:
                object.clear(self.state.con)

            #handle keys and exit game
            # Util.set_player_action(Util.handle_keys(self.state.util))
            Util.handle_keys(self.state.util)
            if Util.get_player_action() == Util.EXIT or self.state.player.color == libtcod.dark_red:
                break

            #let monsters take their turn
            if Util.get_game_state() == Util.PLAYING and Util.get_player_action() != Util.DID_NOT_TAKE_TURN:
                for object in self.state.objects:
                    if object.ai:
                        object.ai.take_turn(self.state.util)
