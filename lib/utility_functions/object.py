__author__ = 'cmotevasselani'

import math

from lib.random_libs import libtcodpy as libtcod
from util import Util


class Object:
  # generic object class: player, monsters, items, etc.
  # the object should always be represented by a char on the screen

  def __init__(self, x, y, char, name, color, always_visible=False, blocks=False, fighter=None, ai=None, item=None,
               equipment=None, caster=None):
    self.always_visible = always_visible
    self.name = name
    self.blocks = blocks
    self.x = x
    self.y = y
    self.char = char
    self.color = color
    self.fighter = fighter
    if self.fighter:  # let the fighter component know who owns it
      self.fighter.owner = self
    self.ai = ai  # let the ai component know who owns it
    if self.ai:
      self.ai.owner = self
    self.item = item  # let the item component know who owns it
    if self.item:
      self.item.owner = self
    self.equipment = equipment
    if self.equipment:
      self.equipment.owner = self
      self.item = self.equipment.item
      self.item.owner = self
    self.caster = caster  # let the ai component know who owns it
    if self.caster:
      self.caster.owner = self

  def move(self, objects, game_map, dx, dy):
    # move by the given amount
    if not game_map.is_blocked(objects, self.x + dx, self.y + dy):
      self.x += dx
      self.y += dy

  def move_away_from_player(self, state):
    adjacent_tiles = Util.get_adjacent_tiles(state, self.x, self.y)
    print 'hihi'
    max_dist_from_player = 0
    target_x = 0
    target_y = 0
    for tile in adjacent_tiles:
      dist_from_player = state.dijkstra_map[tile.x][tile.y]
      if dist_from_player > max_dist_from_player and dist_from_player < 100:
        max_dist_from_player = dist_from_player
        target_x = tile.x
        target_y = tile.y
    self.move_towards(state.objects, state.game_map, target_x, target_y)

  def move_towards(self, objects, game_map, target_x, target_y):
    # vector from this object to the target, and distance
    dx = target_x - self.x
    dy = target_y - self.y
    distance = math.sqrt(dx ** 2 + dy ** 2)

    # normalize to length one and convert to integer to restrict movement to the map grid
    dx = int(round(dx / distance))
    dy = int(round(dy / distance))
    self.move(objects, game_map, dx, dy)

  def distance(self, x, y):
    return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)


  def distance_to(self, other):
    # return the distance to another object
    dx = other.x - self.x
    dy = other.y - self.y
    return math.sqrt(dx ** 2 + dy ** 2)

  def draw(self, state):
    # only show if visible to the player
    if libtcod.map_is_in_fov(state.fov_map, self.x, self.y) or self.always_visible and state.game_map.game_map[self.x][
      self.y].explored:
      # set the color and then draw the char that represents this object at its position
      libtcod.console_set_default_foreground(state.con, self.color)
      libtcod.console_put_char(state.con, self.x, self.y, self.char, libtcod.BKGND_NONE)

  def clear(self, con):
    # erase the character that represents this object
    libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

  def send_to_back(self, objects):
    # make this object be drawn first so that all other objects draw over it
    objects.remove(self)
    objects.insert(0, self)

  def get_info(self, state):
    str = "Name: " + self.name + "\n"
    # Update, try out iterating through over an object's attrs' and check if they have a get_info method, if so, then call it and append + newline
    if self.fighter:
      str += self.fighter.get_info(state) + "\n"
    if self.item:
      str += self.item.get_info(state) + "\n"
    if self.equipment:
      str += self.equipment.get_info(state) + "\n"
    if self.caster:
      str += self.caster.get_info(state) + "\n"
    return str


