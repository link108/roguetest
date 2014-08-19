__author__ = 'cmotevasselani'

from lib import libtcodpy as libtcod

class Console:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.console = libtcod.console_new(width, height)
