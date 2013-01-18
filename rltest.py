# Cameron Motevasselani

import libtcodpy as libtcod
import math

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

MAP_WIDTH = 80
MAP_HEIGHT = 45 
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


class Tile:
    #a tile of the map and its properties

    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        self.explored = False

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

def is_blocked(x, y): 
    #first test the map tile
    if map[x][y].blocked:
        return True

    #now check for any blocking objects
    for object in objects:
        if object.blocks and object.x == x and object.y == y:
            return True
    return False

def player_move_or_attack(dx, dy):
    global fov_recompute

    #the coordinates the player is moving to/attacking
    x = player.x + dx
    y = player.y + dy

    #try tofind an attackable target
    target = None
    for object in objects:
        if object.fighter and object.x == x and object.y == y:
            target = object
            break

    #attack if target found, move otherwise
    if target is not None:
        player.fighter.attack(target)
    else: 
        player.move(dx, dy)
        fov_recompute = True

def handle_keys():
    global fov_recompute

    #key = libtcod.console_check_for_keypress()    #real-time
    key = libtcod.console_wait_for_keypress(True)
    if key.pressed == False:            #to prevent actions from being preformed twice
        return 'didnt-take-turn'

    if key.vk == libtcod.KEY_ENTER and key.lalt:        # Toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    elif key.vk == libtcod.KEY_ESCAPE:                  # exit game
        return 'exit' 

    if game_state == 'playing':
        #movement keys
        if key.vk == libtcod.KEY_CHAR:
            if key.c == ord('k'):
                player_move_or_attack(0, -1)
            elif key.c == ord('j'):
                player_move_or_attack(0, 1)
            elif key.c == ord('h'):
                player_move_or_attack(-1, 0)
            elif key.c == ord('l'):
                player_move_or_attack(1, 0)
            else:
                return 'didnt-take-turn'

class Object: 
    #generic object class: player, monsters, items, etc.
    #the object should always be represented by a char on the screen

    def __init__(self, x, y, char, name, color, blocks = False, fighter = None, ai = None):
        self.name = name
        self.blocks = blocks
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.fighter = fighter
        if self.fighter:    #let the fighter component know who owns it
            self.fighter.owner = self
        self.ai = ai        #let the ai component know who owns it
        if self.ai:
            self.ai.owner = self

    def move(self, dx, dy):
        #move by the given amount
        if not is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

    def move_towards(self, target_x, target_y):
        #vector from this object to the target, and distance
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        #normalize to length one and convert to integer to restrict movement to the map grid
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy)

    def distance_to(self, other):
        #return the distance to another object
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def draw(self):
        #only show if visible to the player
        if libtcod.map_is_in_fov(fov_map, self.x, self.y):
            #set the color and then draw the char that represents this object at its position
            libtcod.console_set_default_foreground(con, self.color)
            libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def clear(self):
        #erase the character that represents this object
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

    def send_to_back(self):
        #make this object be drawn first so that all other objects draw over it
        global objects
        objects.remove(self)
        objects.insert(0, self)

class Fighter:
    #combat related properties and methods (npcs, monsters, player)
    def __init__(self, hp, defense, power, death_function = None):
        self.death_function = death_function
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.death_function = death_function

    def take_damage(self, damage):
        #apply damage if possible
        if damage > 0:
            self.hp -= damage
            if self.hp <= 0:
                function = self.death_function
                if function is not None:
                    function(self.owner)


    def attack(self, target):
        #simple formula for attack damage
        damage = self.power - target.fighter.defense

        if damage > 0:
            #make the target take some damage
            print self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + 'hit points'
            target.fighter.take_damage(damage)
        else:
            print self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!'

class BasicMonster:
    #AI for basic monsters
    def take_turn(self):
        #a basic monster takes its turn. If you can see it, it can see you
        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            #move towards player if far away 
            if monster.distance_to(player) >= 2:
                monster.move_towards(player.x, player.y)

            #attack if close enough
            elif player.fighter.hp > 0:
                monster.fighter.attack(player)

def player_death(player):
    #the game ended, yasd?
    global game_state
    print 'You died!'
    game_state = 'dead'

    #player is a corpse
    player.char = '%' 
    player.color = libtcod.dark_red

def monster_death(monster):
    #monster turns into a corpse, does not block, cant be attacked, does not move
    print monster.name.capitalize() + ' is dead!'
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.send_to_back()

def make_map():
    global map, player

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

            #add some content to this room such as monsters
            place_objects(new_room)

            #get the center coordinates of the new room
            (new_x, new_y) = new_room.center()

            #print the room number (debugging)
            #prints characters rather than numbers, #rooms may be > 10
            room_no = Object(new_x, new_y, chr(65+num_rooms), 'room number', libtcod.white)
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

def place_objects(room):
    #choose random number of monsters
    num_monsters = libtcod.random_get_int(0, 0, MAX_ROOM_MONSTERS)

    for i in range(num_monsters):
        #choose random spot for this monster
        x = libtcod.random_get_int(0, room.x1, room.x2)
        y = libtcod.random_get_int(0, room.y1, room.y2)

        if not is_blocked(x, y):
            if libtcod.random_get_int(0, 0, 100) < 80: #80% chance of getting an orc
                #create an orc
                fighter_component = Fighter(hp=10, defense=0, power=3, death_function = monster_death)
                ai_component = BasicMonster()
                monster = Object(x, y, 'o', 'orc',  libtcod.desaturated_green, blocks = True,
                        fighter = fighter_component, ai = ai_component) 
            else:
                #Create a troll
                fighter_component = Fighter(hp=16, defense=1, power=4, death_function = monster_death)
                ai_component = BasicMonster()
                monster = Object(x, y, 'T', 'troll', libtcod.darker_green, blocks = True, 
                        fighter = fighter_component, ai= ai_component)
            objects.append(monster)

    
def render_all():
    global fov_map 
    global fov_recompute
    global color_dark_wall, color_light_wall
    global color_dark_ground, color_light_ground

    if fov_recompute:
        #recompute FOV if needed 
        fov_recompute = False
        libtcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = map[x][y].block_sight
                if not visible:
                    #if not visible right now, player can only see if explored
                    if map[x][y].explored:
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
                    map[x][y].explored = True


    #draw all objects in the list
    for object in objects:
        if object != player:
            object.draw()
    player.draw()

    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

    #show the player's stats
    libtcod.console_set_default_foreground(con, libtcod.white)
    libtcod.console_print_ex(0, 1, SCREEN_HEIGHT - 2, libtcod.BKGND_NONE, libtcod.LEFT,
            'HP: ' + str(player.fighter.hp) + '/' + str(player.fighter.max_hp))

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'rltest', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

#not real time, but if want it to be a real time game, add next line
#libtcod.sys_set_fps(LIMIT_FPS)

#create the player object
        
fighter_component = Fighter(hp = 30, defense = 2, power = 5, death_function = player_death)
player = Object(0, 0, '@', 'player', libtcod.white, blocks = True, fighter = fighter_component)
#the list of all objects
objects = [player]
make_map()
fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)

fov_recompute = True
game_state = 'playing'
player_action = None

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
    player_action = handle_keys()
    if player_action == 'exit': 
        break

    #let monsters take their turn
    if game_state == 'playing' and player_action != 'didnt-take-turn':
        for object in objects:
            if object.ai:
                object.ai.take_turn()
