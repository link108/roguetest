# Cameron Motevasselani
from lib import libtcodpy as libtcod

from lib.object import Object
from lib.util import Util
from lib.fighter import Fighter
from lib.map import Map
from lib.inventory import Inventory
from lib.consoles.status_panel import StatusPanel

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

color_dark_wall = libtcod.Color(0, 0, 100)
color_light_wall = libtcod.Color(130, 110, 50)
color_dark_ground = libtcod.Color(50, 50, 150)
color_light_ground = libtcod.Color(200, 180, 50)

util = Util()

def render_all(game_map, fov_map, fov_recompute, status_panel):
    global color_dark_wall, color_light_wall
    global color_dark_ground, color_light_ground

    if fov_recompute:
        #recompute FOV if needed 
        fov_recompute = False
        libtcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.get_map()[x][y].block_sight
                if not visible:
                    #if not visible right now, player can only see if explored
                    if game_map.get_map()[x][y].explored:
                        if wall:
                            libtcod.console_set_char_background(con, x, y, color_dark_wall, libtcod.BKGND_SET)
                        else: 
                            libtcod.console_set_char_background(con, x, y, color_dark_ground, libtcod.BKGND_SET)
                else: 
                    #it is visible
                    if wall:
                        libtcod.console_set_char_background(con, x, y, color_light_wall, libtcod.BKGND_SET)
                    else: 
                        libtcod.console_set_char_background(con, x, y, color_light_ground, libtcod.BKGND_SET)
                    game_map.get_map()[x][y].explored = True


    #draw all objects in the list
    for object in objects:
        if object != player:
            object.draw(fov_map, con)
    player.draw(fov_map, con)

    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

    #prepare to render the GUI panel
    libtcod.console_set_default_background(status_panel.get_panel(), libtcod.black)
    libtcod.console_clear(status_panel.get_panel())

    #print the game messages, one line at a time
    y = 1
    for (line, color) in status_panel.game_messages:
        libtcod.console_set_default_foreground(status_panel.get_panel(), color)
        libtcod.console_print_ex(status_panel.get_panel(), MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
        y += 1
    #show the player's stats
    status_panel.render_bar(1, 1, BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp,
        libtcod.light_red, libtcod.darker_red)

    #blit the contents of "panel" to the root console
    libtcod.console_blit(status_panel.get_panel(), 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)

    #show the player's stats
    # libtcod.console_set_default_foreground(con, libtcod.white)
    # libtcod.console_print_ex(0, 1, SCREEN_HEIGHT - 2, libtcod.BKGND_NONE, libtcod.LEFT,
    #         'HP: ' + str(player.fighter.hp) + '/' + str(player.fighter.max_hp))

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'rltest', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

status_panel = StatusPanel(SCREEN_WIDTH, PANEL_HEIGHT, MSG_WIDTH, MSG_HEIGHT)

#a warm welcoming message!
status_panel.message('Welcome stranger! Prepare to perish in the Tombs of the Ancient Kings.', libtcod.red)
#create the player object
        
fighter_component = Fighter(hp = 30, defense = 2, power = 5, death_function = Util.player_death)
player = Object(0, 0, '@', 'player', libtcod.white, blocks = True, fighter = fighter_component)
#the list of all objects
objects = [player]
player_inventory = Inventory(status_panel, objects)
game_map = Map(status_panel, player)
game_map.make_map(objects, player)
fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
util.set_attr(player, status_panel, fov_map, objects, player_inventory, game_map)
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        libtcod.map_set_properties(fov_map, x, y, not game_map.is_blocked_sight(objects, x, y), not game_map.is_blocked_sight(objects, x, y))
        # libtcod.map_set_properties(fov_map, x, y, not game_map[x][y].is_blocked_sight, not game_map[x][y].is_blocked_sight)

fov_recompute = True
game_state = 'playing'
player_action = None

###########################################
#main loop
###########################################
while not libtcod.console_is_window_closed():

    render_all(game_map, fov_map, fov_recompute, status_panel)

    libtcod.console_flush()

    #erase all objects at their old locations, before they move
    for object in objects:
        object.clear(con)

    #handle keys and exit game 
    player_action = util.handle_keys(game_state, con, SCREEN_WIDTH, SCREEN_HEIGHT, util)
    if player_action == 'exit' or player.color == libtcod.dark_red:
        break

    #let monsters take their turn
    if game_state == 'playing' and player_action != 'didnt-take-turn':
        for object in objects:
            if object.ai:
                object.ai.take_turn(util)
