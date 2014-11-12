from lib import libtcodpy as libtcod

__author__ = 'cmotevasselani'

from lib.tile import Tile
from lib.rectangle import Rect
from lib.object import Object
from lib.fighter import Fighter
from lib.basic_monster import BasicMonster
from lib.item import Item
from lib.util import Util
from lib.constants.map_constants import MapConstants
from lib.constants.constants import Constants
from lib.ai.confused_monster import ConfusedMonster

###### NOTE ######
#### not a fan of this implementation, I couldn't find another way of saving/loading funtions
#### unless they were not in a class. Suggestions are welcome
#### -Cameron

###### ScrollFunctions

def cast_fireball(state):
    # TODO: Add range check
    x, y = Util.target_tile(state)
    state.game_map.get_map()[x][y].set_targeted(False)
    for object in state.objects:
        if object.distance(x,y) <= Constants.FIREBALL_RADIUS and object.fighter:
            state.status_panel.message('You sling a fireball at: ' + object.name + ' with a BAMboosh! The damage done is '
                                + str(Constants.FIREBALL_DAMAGE) + ' hp.', libtcod.light_blue)
            object.fighter.take_damage(Constants.FIREBALL_DAMAGE, state)

def cast_confuse(state):
    # monster = Constants.closest_monster(util, Constants.CONFUSE_RANGE)
    monster = Util.target_monster(state, Constants.CONFUSE_RANGE)
    if monster is None:
        state.status_panel.message('No enemy is close enough to confuse', libtcod.red)
        return Constants.CANCELLED
    old_ai = monster.ai
    monster.ai = ConfusedMonster(old_ai, state)
    monster.clear(state.con)
    monster.ai.owner = monster
    state.status_panel.message('The eyes of the ' + monster.name + ' look vacant, as he starts to stumble around!', libtcod.light_green)

def cast_lightning(state):
    monster = Util.closest_monster(state, Constants.LIGHTNING_RANGE)
    if monster is None:
        state.status_panel.message('No enemy is close enough to strike with lightning', libtcod.red)
        return Constants.CANCELLED
    state.status_panel.message('A lightning bolt strikes the ' + monster.name + ' with a ZAP! The damage done is '
                        + str(Constants.LIGHTNING_DAMAGE) + ' hp.', libtcod.light_blue)
    monster.fighter.take_damage(Constants.LIGHTNING_DAMAGE, state)


##### DeathFunctions

def monster_death(monster, state):
    #monster turns into a corpse, does not block, cant be attacked, does not move
    state.status_panel.message(monster.name.capitalize() + ' is dead! You gain ' + str(monster.fighter.xp) + ' xp!', libtcod.white)
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.send_to_back(state.objects)


###### PotionFunctions

def cast_heal(state):
    if state.player.fighter.hp == state.player.fighter.max_hp:
        state.status_panel.message('You are already at full health.', libtcod.red)
        return Constants.CANCELLED
    state.status_panel.message('Your wounds start to feel better', libtcod.light_violet)
    state.player.fighter.heal(Constants.HEAL_AMOUNT)

class Map:

    def __init__(self, state):
        self.status_panel = state.status_panel
        self.player = state.player
        self.game_map = None


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
        monster_chances = {
            MapConstants.ORC: 80,
            MapConstants.TROLL: 20
        }
        item_chances = {
            MapConstants.HEALTH_POTION: 7,
            MapConstants.SCROLL_OF_LIGHTNING_BOLT: 10,
            MapConstants.SCROLL_OF_FIREBALL: 10,
            MapConstants.SCROLL_OF_CONFUSE: 100
        }
        num_monsters = libtcod.random_get_int(0, 0, MapConstants.MAX_ROOM_MONSTERS)

        for i in range(num_monsters):
            #choose random spot for this monster
            x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
            y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)

            if not self.is_blocked(objects, x, y):
                choice = Util.random_choice(monster_chances)
                if choice == MapConstants.ORC:
                    #create an orc
                    fighter_component = Fighter(hp=10, defense=0, power=3, xp=35, death_function=monster_death)
                    ai_component = BasicMonster()
                    monster = Object(x, y, 'o', MapConstants.ORC,  libtcod.desaturated_green, blocks=True,
                                    fighter=fighter_component, ai=ai_component)
                elif choice == MapConstants.TROLL:
                    #Create a troll
                    fighter_component = Fighter(hp=16, defense=1, power=4, xp=100, death_function=monster_death)
                    ai_component = BasicMonster()
                    monster = Object(x, y, 'T', MapConstants.TROLL, libtcod.darker_green, blocks=True,
                                    fighter=fighter_component, ai=ai_component)
                objects.append(monster)

        #choose random number of items
        num_items = libtcod.random_get_int(0, 0, MapConstants.MAX_ROOM_ITEMS)

        for i in range(num_items):
            #choose random spot for this item
            x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
            y = libtcod.random_get_int(0, room.y1+1, room.y2-1)

            #only place it if the tile is not blocked
            if not self.is_blocked(objects, x, y):
                choice = Util.random_choice(item_chances)
                if choice == MapConstants.HEALTH_POTION:
                    #create a healing potion
                    item_component = Item(use_function=cast_heal)
                    item = Object(x, y, '!', MapConstants.HEALTH_POTION, libtcod.violet, item=item_component, always_visible=True)
                elif choice == MapConstants.SCROLL_OF_FIREBALL:
                    item_component = Item(use_function=cast_fireball)
                    item = Object(x, y, '#', MapConstants.SCROLL_OF_FIREBALL, libtcod.light_yellow, item=item_component, always_visible=True)
                elif choice == MapConstants.SCROLL_OF_CONFUSE:
                    item_component = Item(use_function=cast_confuse)
                    item = Object(x, y, '#', MapConstants.SCROLL_OF_CONFUSE, libtcod.light_yellow, item=item_component, always_visible=True)
                elif choice == MapConstants.SCROLL_OF_LIGHTNING_BOLT:
                    item_component = Item(use_function=cast_lightning)
                    item = Object(x, y, '#', MapConstants.SCROLL_OF_LIGHTNING_BOLT, libtcod.light_yellow, item=item_component, always_visible=True)

                objects.append(item)
                item.send_to_back(objects)  #items appear below other objects


    def make_map(self, state):
        # global map, player
        #fill map with "unblocked" tiles
        # self.map = [[ Tile(True)
        #     for y in range(MAP_HEIGHT) ]
        #         for x in range(MAP_WIDTH) ]

        self.game_map = [[ Tile(True)
            for y in range(MapConstants.MAP_HEIGHT) ]
                for x in range(MapConstants.MAP_WIDTH) ]
        rooms = []
        num_rooms = 0
        for r in range(MapConstants.MAX_ROOMS):
            #random width and height
            w = libtcod.random_get_int(0, MapConstants.ROOM_MIN_SIZE, MapConstants.ROOM_MAX_SIZE)
            h = libtcod.random_get_int(0, MapConstants.ROOM_MIN_SIZE, MapConstants.ROOM_MAX_SIZE)
            x = libtcod.random_get_int(0, 0, MapConstants.MAP_WIDTH - w - 1)
            y = libtcod.random_get_int(0, 0, MapConstants.MAP_HEIGHT -h - 1)

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
                self.place_objects(new_room, state.objects)

                #get the center coordinates of the new room
                (new_x, new_y) = new_room.center()

                #print the room number (debugging)
                #prints characters rather than numbers, #rooms may be > 10
                # room_no = Object(new_x, new_y, chr(65+num_rooms), 'room number', libtcod.white)
                # objects.insert(0, room_no) #draw early so monsters are drawn on top

                if num_rooms == 0:
                    #this is the first room, where the player starts at
                    state.player.x = new_x
                    state.player.y = new_y
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
        stairs = Object(new_x, new_y, MapConstants.STAIRS_OBJECT, MapConstants.STAIRS_NAME, MapConstants.STAIRS_COLOR, always_visible=True)
        state.objects.append(stairs)
        stairs.send_to_back(state.objects)
        state.stairs = stairs

    def get_map(self):
        return self.game_map


