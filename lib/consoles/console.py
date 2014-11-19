from lib.random_libs import libtcodpy as libtcod

__author__ = 'cmotevasselani'


class Console:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.console = libtcod.console_new(width, height)
