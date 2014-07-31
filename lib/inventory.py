__author__ = 'cmotevasselani'

class Inventory:

    def __init__(self, status_panel, objects):
        self.status_panel = status_panel
        self.inventory = []
        self.objects = objects

    def get_status_panel(self):
        return self.status_panel
