__author__ = 'cmotevasselani'

from lib import libtcodpy as libtcod
from lib.consoles.console import Console
import textwrap

class StatusPanel():

    def __init__(self, screen_width, panel_height, message_width, message_height):
        self.panel = Console(screen_width, panel_height)
        self.game_messages = []
        self.message_width = message_width
        self.message_height = message_height

    def get_panel(self):
        return self.panel.console

    def get_game_messages(self):
        return self.game_messages

    def render_bar(self, x, y, total_width, name, value, maximum, bar_color, back_color):
        #render a bar (HP, experience, etc). first calculate the width of the bar
        bar_width = int(float(value) / maximum * total_width)

        #render the background first
        libtcod.console_set_default_background(self.panel.console, back_color)
        libtcod.console_rect(self.panel.console, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

        #now render the bar on top
        libtcod.console_set_default_background(self.panel.console, bar_color)
        if bar_width > 0:
            libtcod.console_rect(self.panel.console, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

        #finally, some centered text with the values
        libtcod.console_set_default_foreground(self.panel.console, libtcod.white)
        libtcod.console_print_ex(self.panel.console, x + total_width / 2, y, libtcod.BKGND_NONE, libtcod.CENTER,
            name + ': ' + str(value) + '/' + str(maximum))

    def message(self, new_message, color = libtcod.white):
        #split the message if necessary, among multiple lines
        new_msg_lines = textwrap.wrap(new_message, self.message_width)

        for line in new_msg_lines:
            #if the buffer is full, remove the first line to make room for the new one
            if len(self.game_messages) == self.message_height:
                del self.game_messages[0]

            #add the new line as a tuple, with the text and the color
            self.game_messages.append( (line, color) )
