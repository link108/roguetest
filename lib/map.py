from lib import libtcodpy as libtcod

__author__ = 'cmotevasselani'

from lib.scroll_functions import ScrollFunctions
from lib.potion_functions import PotionFunctions
from lib.tile import Tile
from lib.rectangle import Rect
from lib.object import Object
from lib.util import Util
from lib.fighter import Fighter
from lib.basic_monster import BasicMonster
from lib.item import Item


SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

MAP_WIDTH = 80
MAP_HEIGHT = 45
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
MAX_ROOM_ITEMS = 2

FOV_ALGO = 0    #default FOV algorithm
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10
MAX_ROOM_MONSTERS = 3

color_dark_wall = libtcod.Color(0, 0, 100)
color_light_wall = libtcod.Color(130, 110, 50)
color_dark_ground = libtcod.Color(50, 50, 150)
color_light_ground = libtcod.Color(200, 180, 50)

class Map:

    def __init__(self, status_panel, player):
        self.status_panel = status_panel
        self.player = player
        self.game_map = [[ Tile(True)
            for y in range(MAP_HEIGHT) ]
                for x in range(MAP_WIDTH) ]

    def get_objects(self):
        return self.objects

    def get_status_panel(self):
        return self.status_panel

    def is_blocked(self, objects, x, y):
        #first test the map tile
        if self.game_map[x][y].blocked:
            return True

        #now check for any blocking objects
        for object in objects:
            if object.blocks and object.x == x and object.y == y:
                return True
        return False

    def is_blocked_sight(self, objects, x, y):
        #first test the map tile
        if self.game_map[x][y].block_sight:
            return True

        #now check for any blocking objects
        for object in objects:
            if object.blocks and object.x == x and object.y == y:
                return True
        return False

    def create_room(self, room):
        # global map
        #go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.game_map[x][y].set_blocked(False)
                self.game_map[x][y].set_block_sight(False)

    def create_h_tunnel(self, x1, x2, y):
        # global map
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.game_map[x][y].set_blocked(False)
            self.game_map[x][y].set_block_sight(False)

    def create_v_tunnel(self, y1, y2, x):
        # global map
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.game_map[x][y].set_blocked(False)
            self.game_map[x][y].set_block_sight(False)

    def place_objects(self, room, objects):
        #choose random number of monsters
        num_monsters = libtcod.random_get_int(0, 0, MAX_ROOM_MONSTERS)

        for i in range(num_monsters):
            #choose random spot for this monster
            x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
            y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)

            if not self.is_blocked(objects, x, y):
                if libtcod.random_get_int(0, 0, 100) < 80: #80% chance of getting an orc
                    #create an orc
                    fighter_component = Fighter(hp=10, defense=0, power=3, death_function = Util.monster_death)
                    ai_component = BasicMonster()
                    monster = Object(x, y, 'o', 'orc',  libtcod.desaturated_green, blocks = True,
                            fighter = fighter_component, ai = ai_component)
                else:
                    #Create a troll
                    fighter_component = Fighter(hp=16, defense=1, power=4, death_function = Util.monster_death)
                    ai_component = BasicMonster()
                    monster = Object(x, y, 'T', 'troll', libtcod.darker_green, blocks = True,
                            fighter = fighter_component, ai= ai_component)
                objects.append(monster)

        #choose random number of items
        num_items = libtcod.random_get_int(0, 0, MAX_ROOM_ITEMS)

        for i in range(num_items):
            #choose random spot for this item
            x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
            y = libtcod.random_get_int(0, room.y1+1, room.y2-1)

            #only place it if the tile is not blocked
            if not self.is_blocked(objects, x, y):
                dice = libtcod.random_get_int(0, 0, 100)
                if dice < 10:
                    #create a healing potion
                    item_component = Item(use_function=PotionFunctions.cast_heal)
                    item = Object(x, y, '!', 'healing potion', libtcod.violet, item=item_component)
                elif dice < 99:
                    item_component = Item(use_function=ScrollFunctions.cast_confuse)
                    item = Object(x, y, '#', 'scorr of CONFUSE', libtcod.light_yellow, item=item_component)
                else:
                    item_component = Item(use_function=ScrollFunctions.cast_lightning)
                    item = Object(x, y, '#', 'scroll of LIGHTNING BOLT', libtcod.light_yellow, item=item_component)

                objects.append(item)
                item.send_to_back(objects)  #items appear below other objects


    def make_map(self, objects, player):
        # global map, player

        #fill map with "unblocked" tiles
        # self.map = [[ Tile(True)
        #     for y in range(MAP_HEIGHT) ]
        #         for x in range(MAP_WIDTH) ]

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
                self.create_room(new_room)

                #add some content to this room such as monsters
                self.place_objects(new_room, objects)

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
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        #move vertically first, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                #finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

    def get_map(self):
        return self.game_map


