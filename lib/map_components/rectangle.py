__author__ = 'cmotevasselani'

import random


class Rect:
  # a rectangle on the map, used for a room (usually)
  def __init__(self, x, y, w, h):
    self.x1 = x
    self.y1 = y
    self.x2 = x + w
    self.y2 = y + h
    self.center_x = (self.x1 + self.x2) / 2
    self.center_y = (self.y1 + self.y2) / 2

  def center(self):
    return self.center_x, self.center_y

  def center_x(self):
    return self.center_x

  def center_y(self):
    return self.center_y

  def intersect(self, other):
    # returns true if this rectangle intersects with another one
    return (self.x1 <= other.x2 and self.x2 >= other.x1 and
            self.y1 <= other.y2 and self.y2 >= other.y1)


  def get_random_point(self):
    x = random.randint(self.x1 + 1, self.x2 - 1 )
    y = random.randint(self.y1 + 1, self.y2 - 1)
    return x, y
