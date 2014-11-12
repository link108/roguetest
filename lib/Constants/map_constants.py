__author__ = 'cmotevasselani'

from lib import libtcodpy as libtcod

class MapConstants:

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
    MAX_ROOM_ITEMS = 7

    FOV_ALGO = 0    #default FOV algorithm
    FOV_LIGHT_WALLS = True
    TORCH_RADIUS = 10
    MAX_ROOM_MONSTERS = 3

    COLOR_DARK_WALL = libtcod.Color(0, 0, 100)
    COLOR_LIGHT_WALL = libtcod.Color(130, 110, 50)
    COLOR_DARK_GROUND = libtcod.Color(50, 50, 150)
    COLOR_lIGHT_GROUND = libtcod.Color(200, 180, 50)
    COLOR_TARGETED = libtcod.green

    STAIRS_COLOR = libtcod.white
    STAIRS_NAME = 'stairs'
    STAIRS_OBJECT = '>'

    LEVEL_SCREEN_WIDTH = 40
    CHARACTER_SCREEN_WIDTH = 30


    #Monsters
    TROLL = 'troll'
    ORC = 'orc'


    #Items
    HEALTH_POTION = 'health potion'
    SCROLL_OF_FIREBALL = 'scroll of fireball'
    SCROLL_OF_CONFUSE = 'scroll of confuse'
    SCROLL_OF_LIGHTNING_BOLT = 'scroll of lightning-bolt'




