__author__ = 'cmotevasselani'

from lib import libtcodpy as libtcod

from lib.object import Object
from lib.fighter import Fighter
from lib.map import Map
from lib.inventory import Inventory
from lib.consoles.status_panel import StatusPanel
from lib.map_constants import MapConstants
from lib.util import Util

class State:

    def __init__(self):
        libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
        libtcod.console_init_root(MapConstants.SCREEN_WIDTH, MapConstants.SCREEN_HEIGHT, 'rltest', False)
        self.con = libtcod.console_new(MapConstants.SCREEN_WIDTH, MapConstants.SCREEN_HEIGHT)
        self.status_panel = StatusPanel(MapConstants.SCREEN_WIDTH,MapConstants.PANEL_HEIGHT, MapConstants.MSG_WIDTH, MapConstants.MSG_HEIGHT)
        self.util = None
        self.fov_map = None
        self.fov_recompute = True
        self.game_map = None
        self.objects = None
        self.player = None
        self.player_inventory = None

    def new_game(self):
        #a warm welcoming message!
        self.status_panel.message('Welcome stranger! Prepare to perish in the Tombs of the Ancient Kings.', libtcod.red)
        self.util = Util()

        #create the player object

        # fighter_component = Fighter(hp = 30, defense = 2, power = 5, death_function = Util.player_death)
        fighter_component = Fighter(hp=300, defense=20, power=50, death_function=Util.player_death)
        self.player = Object(0, 0, '@', 'player', libtcod.white, blocks=True, fighter=fighter_component)
        #the list of all objects
        self.objects = [self.player]
        self.player_inventory = Inventory(self.status_panel, self.objects, self.player)
        self.game_map = Map(self.status_panel, self.player)
        self.game_map.make_map(self.objects, self.player)
        self.initialize_fov()
        self.util.set_attr(self.player, self.status_panel, self.fov_map, self.objects, self.player_inventory, self.game_map, self.con)

    def initialize_fov(self):
        self.fov_map = libtcod.map_new(MapConstants.MAP_WIDTH, MapConstants.MAP_HEIGHT)
        for y in range(MapConstants.MAP_HEIGHT):
            for x in range(MapConstants.MAP_WIDTH):
                libtcod.map_set_properties(self.fov_map, x, y, not self.game_map.is_blocked_sight(self.objects, x, y), not self.game_map.is_blocked_sight(self.objects, x, y))
                # libtcod.map_set_properties(fov_map, x, y, not game_map[x][y].is_blocked_sight, not game_map[x][y].is_blocked_sight)

    def play_game(self):

        player_action = None
        Util.set_game_state(Util.PLAYING)

        ###########################################
        #main loop
        ###########################################
        while not libtcod.console_is_window_closed():

            Util.render_all(self.util, self.fov_recompute)
            libtcod.console_flush()

            #erase all objects at their old locations, before they move
            for object in self.objects:
                object.clear(self.con)

            #handle keys and exit game
            Util.set_player_action(Util.handle_keys(self.util))
            if Util.get_player_action() == Util.EXIT or self.player.color == libtcod.dark_red:
                break

            #let monsters take their turn
            if Util.get_game_state() == Util.PLAYING and Util.get_player_action() != Util.DID_NOT_TAKE_TURN:
                for object in self.objects:
                    if object.ai:
                        object.ai.take_turn(self.util)