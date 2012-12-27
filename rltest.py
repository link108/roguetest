# Cameron Motevasselani

import libtcodpy as libtcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

MAP_WIDTH = 80
MAP_HEIGHT = 45 

color_dark_wall = libtcod.Color(0, 0, 100)
color_dark_ground = libtcod.Color(50, 50, 150)

class Tile:
    #a tile of the map and its properties

    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked

        #by default, if a tile is blocked, also blocks sight
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight


def handle_keys():

    #key = libtcod.console_check_for_keypress()    #real-time
    key = libtcod.console_wait_for_keypress(True)
    if key.pressed == False:            #to prevent actions from being preformed twice
        return False

    if key.vk == libtcod.KEY_ENTER and key.lalt:        # Toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    elif key.vk == libtcod.KEY_ESCAPE:                  # exit game
        return True    

    #movement keys
    if key.vk == libtcod.KEY_CHAR:
        if key.c == ord('k'):
            player.move(0, -1)
        elif key.c == ord('j'):
            player.move(0, 1)
        elif key.c == ord('h'):
            player.move(-1, 0)
        elif key.c == ord('l'):
            player.move(1, 0)

class Object: 
    #generic object class: player, monsters, items, etc.
    #it's (the object) is always represented by a char on the screen

    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        #move by the given amount
        if not map[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy

    def draw(self):
        #set the color and then draw the char that represents this object at its position
        libtcod.console_set_default_foreground(con, self.color)
        libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def clear(self):
        #erase the character that represents this object
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

def make_map():
    global map

    #fill map with "unblocked" tiles
    map = [[ Tile(False)
        for y in range(MAP_HEIGHT) ]
            for x in range(MAP_WIDTH) ]

    map[30][22].blocked = True
    map[30][22].block_sight = True
    map[50][22].blocked = True
    map[50][22].block_sight = True
    
def render_all():
    #draw all objects in the list
    for object in objects:
        object.draw()
    
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = map[x][y].block_sight
            if wall:
                libtcod.console_set_char_background(con, x, y, color_dark_wall, libtcod.BKGND_SET)
            else: 
                libtcod.console_set_char_background(con, x, y, color_dark_ground, libtcod.BKGND_SET)
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'rltest', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

#not real time, but if want it to be a real time game, add next line
#libtcod.sys_set_fps(LIMIT_FPS)

player = Object(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', libtcod.white)
npc = Object(SCREEN_WIDTH/2 - 5, SCREEN_HEIGHT/2, '@', libtcod.yellow)
objects = [npc, player]
make_map()

###########################################
#main loop
###########################################
while not libtcod.console_is_window_closed():

    render_all()

    libtcod.console_flush()

    #erase all objects at their old locations, before they move
    for object in objects:
        object.clear()

    #handle keys and exit game 
    exit = handle_keys()
    if exit: 
        break
