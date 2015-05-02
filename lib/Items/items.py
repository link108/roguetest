__author__ = 'cmotevasselani'

import copy
from item_functions.potion_functions import PotionFunctions
from item_functions.scroll_functions import ScrollFunctions
from lib.constants.constants import Constants
from item import Item

class Items:

    def __init__(self):
        self.items = {}
        self.init_items()

    def init_items(self):
        with open(Constants.ITEM_FILE) as f:
            item_file = f.readlines()
        for line in item_file:
            if not line[0] == '#':
                line_array = line.split(' ')
                item_name = line_array[0]
                item_info = line_array[1]
                item = Item(item_name, item_info)
                self.items[item_name] = item

    def get_item(self, item_name):
        return copy.deepcopy(self.items[item_name])
