__author__ = 'cmotevasselani'


import datetime
from lib.map_components.map import Map
from lib.utility_functions.state import State


state = State()


map = Map()
state.game_map = map

start_time = datetime.datetime.now()
for i in range(100):
  map.create_map_layout(state, i)

end_time = datetime.datetime.now()


diff = end_time - start_time


print "total time taken: " + str(diff)
