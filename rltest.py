# Cameron Motevasselani

import libtcodpy as libtcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

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
        self.x += dx
        self.y += dy

    def draw(self):
        #set the color and then draw the char that represents this object at its position
        libtcod.console_set_default_foreground(con, self.color)
        libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def clear(self):
        #erase the character that represents this object
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'rltest', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

#not real time, but if want it to be a real time game, add next line
#libtcod.sys_set_fps(LIMIT_FPS)

player = Object(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', libtcod.white)
npc = Object(SCREEN_WIDTH/2 - 5, SCREEN_HEIGHT/2, '@', libtcod.yellow)
objects = [npc, player]

###########################################
#main loop
###########################################
while not libtcod.console_is_window_closed():

    #draw all the objects on the list
    for object in objects:
        object.draw()

    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    libtcod.console_flush()

    #erase all objects at their old locations, before they move
    for object in objects:
        object.clear()

    #handle keys and exit game 
    exit = handle_keys()
    if exit: 
        break
