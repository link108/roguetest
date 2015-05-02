__author__ = 'cmotevasselani'

import copy
from lib.constants.constants import Constants
from lib.items.equipment import Equipment

class Equipments:

    def __init__(self):
        self.equipments = {}
        self.init_equipments()

    def init_equipments(self):
        with open(Constants.EQUIPMENT_FILE) as f:
            equipment_file = f.readlines()
        for line in equipment_file:
            if not line[0] == '#':
                line_array = line.split(' ')
                equipment_name = line_array[0]
                equipment_info = line_array[1]
                equipment = Equipment(equipment_name, equipment_info)
                self.equipments[equipment_name] = equipment

    def get_equipment(self, equipment_name):
        return copy.deepcopy(self.equipments[equipment_name])
