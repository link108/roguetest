# Cameron Motevasselani

import libtcodpy as libtcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

MAP_WIDTH = 80
MAP_HEIGHT = 45 
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

color_dark_wall = libtcod.Color(0, 0, 100)
color_dark_ground = libtcod.Color(50, 50, 150)

class Tile:
    #a tile of the map and its properties

    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked

        #by default, if a tile is blocked, also blocks sight
        if block_sight is None: block_sight = blocked           #must specify block_sight is false to get transparent, impassable tiles 
        self.block_sight = block_sight

class Rect:
    #a rectangl on the map, used for a room (usually)
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        #returns center of room
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)

    def intersect(self, other):
        #returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

def create_room(room):
    global map
    #go through the tiles in the rectangle and make them passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            map[x][y].blocked = False
            map[x][y].block_sight = False

def create_h_tunnel(x1, x2, y):
    global map
    for x in range(min(x1, x2), max(x1, x2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False

def create_v_tunnel(y1, y2, x):
    global map
    for y in range(min(y1, y2), max(y1, y2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False

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
    #the object should always be represented by a char on the screen

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
    map = [[ Tile(True)
        for y in range(MAP_HEIGHT) ]
            for x in range(MAP_WIDTH) ]

    rooms = []
    num_rooms = 0
    for r in range(MAX_ROOMS):
        #random width and height
        w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        x = libtcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
        y = libtcod.random_get_int(0, 0, MAP_HEIGHT -h - 1)

        new_room = Rect(x, y, w, h)

        #run through the other rooms to see if they overlap
        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break
        if not failed:
            #no intersections, create the room!
            create_room(new_room)

            #get the center coordinates of the new room
            (new_x, new_y) = new_room.center()

            #print the room number (debugging)
            #prints characters rather than numbers, #rooms may be > 10
            room_no = Object(new_x, new_y, chr(65+num_rooms), libtcod.white)
            objects.insert(0, room_no) #draw early so monsters are drawn on top

            if num_rooms == 0:
                #this is the first room, where the player starts at
                player.x = new_x
                player.y = new_y
            else:
                #all rooms after the first
                #connect it to the previous room with a tunnel

                #center coordinates of the previous room
                (prev_x, prev_y) = rooms[num_rooms - 1].center()

                #flip a coin
                if libtcod.random_get_int(0, 0, 1) == 1:
                    #move horizontally first, then vertically
                    create_h_tunnel(prev_x, new_x, prev_y)
                    create_v_tunnel(prev_y, new_y, new_x)
                else: 
                    #move vertically first, then horizontally
                    create_v_tunnel(prev_y, new_y, prev_x)
                    create_h_tunnel(prev_x, new_x, new_y)

            #finally, append the new room to the list
            rooms.append(new_room)
            num_rooms += 1

    
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
