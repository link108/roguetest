__author__ = 'cmotevasselani'

from lib.consoles.console import Console
from lib import libtcodpy as libtcod


class Menu:

    def display_menu(self, header, options, width, con, screen_width, screen_height):
        if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')
        #calculate total height for the header (after auto-wrap) and one line per option
        header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
        height = len(options) + header_height

        #create an off-screen console that represents the menu's window
        window = libtcod.console_new(width, height)

        #print the header, with auto-wrap
        libtcod.console_set_default_foreground(window, libtcod.white)
        libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

        #print all the options
        y = header_height
        letter_index = ord('a')
        for option_text in options:
            text = '(' + chr(letter_index) + ') ' + option_text
            libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
            y += 1
            letter_index += 1

        #blit the contents of "window" to the root console
        x = screen_width/2 - width/2
        y = screen_height/2 - height/2
        libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

        #present the root console to the player and wait for a key-press
        libtcod.console_flush()
        key = libtcod.console_wait_for_keypress(True)

        #convert the ASCII code to an index; if it corresponds to an option, return it
        index = key.c - ord('a')
        if index >= 0 and index < len(options): return index
        return None