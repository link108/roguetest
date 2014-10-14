__author__ = 'cmotevasselani'

import math

from util import *


class Object:
    #generic object class: player, monsters, items, etc.
    #the object should always be represented by a char on the screen

    def __init__(self, x, y, char, name, color, blocks=False, fighter=None, ai=None, item=None):
        self.name = name
        self.blocks = blocks
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.fighter = fighter
        if self.fighter:    # let the fighter component know who owns it
            self.fighter.owner = self
        self.ai = ai        # let the ai component know who owns it
        if self.ai:
            self.ai.owner = self
        self.item = item        # let the item component know who owns it
        if self.item:
            self.item.owner = self

    def move(self, objects, game_map, dx, dy):
        #move by the given amount
        if not game_map.is_blocked(objects, self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

    def move_towards(self, objects, game_map, target_x, target_y):
        #vector from this object to the target, and distance
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        #normalize to length one and convert to integer to restrict movement to the map grid
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(objects, game_map, dx, dy)

    def distance_to(self, other):
        #return the distance to another object
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def draw(self, fov_map, con):
        #only show if visible to the player
        if libtcod.map_is_in_fov(fov_map, self.x, self.y):
            #set the color and then draw the char that represents this object at its position
            libtcod.console_set_default_foreground(con, self.color)
            libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def clear(self, con):
        #erase the character that represents this object
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

    def send_to_back(self, objects):
        #make this object be drawn first so that all other objects draw over it
        objects.remove(self)
        objects.insert(0, self)
