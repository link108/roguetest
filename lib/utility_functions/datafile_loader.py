__author__ = 'cmotevasselani'

import copy


class DatafileLoader:

  def __init__(self, data_file, data_class, map_name):
    self.data_file = data_file
    self.data_class = data_class
    # self.data_class = eval(data_class)
    self.map_name = map_name
    setattr(self, self.map_name, {})
    # self.object_map = {}
    self.init_objects()

  def init_objects(self):
    with open(self.data_file) as f:
      data_file = f.readlines()
    for line in data_file:
      if not line[0] == '#':
        line_array = line.split(' ')
        data_name = line_array[0]
        data_info = line_array[1]
        data_object = self.data_class(data_name, data_info)
        getattr(self, self.map_name)[data_name] = data_object
        # self.object_map[data_name] = data_object

  def get_data_object(self, object_name):
    # return copy.deepcopy(self.object_map[object_name])
    return copy.deepcopy(getattr(self, self.map_name)[object_name])