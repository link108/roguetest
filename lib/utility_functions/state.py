from lib.random_libs import libtcodpy as libtcod

__author__ = 'cmotevasselani'

from lib.consoles.status_panel import StatusPanel
from lib.constants.map_constants import MapConstants

class State:

    def __init__(self):
        libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
        libtcod.console_init_root(MapConstants.SCREEN_WIDTH, MapConstants.SCREEN_HEIGHT, 'rltest', False)
        self.con = libtcod.console_new(MapConstants.SCREEN_WIDTH, MapConstants.SCREEN_HEIGHT)
        self.status_panel = StatusPanel(MapConstants.SCREEN_WIDTH,MapConstants.PANEL_HEIGHT, MapConstants.MSG_WIDTH, MapConstants.MSG_HEIGHT)
        self.util = None
        self.fov_map = None
        self.fov_map_map = {}
        self.fov_recompute = True
        self.game_map = None
        self.objects = None
        self.objects_map = {}
        self.player = None
        self.player_inventory = None
        self.player_spell_inventory = None
        self.stairs = {}
        self.dungeon_level = None
        self.turn = None
        self.magic = None
        self.player_class = None
        self.player_race = None
        self.items = None
        self.score = None
        self.high_scores = None
        self.monsters = None
        self.equipment = None

