__author__ = 'cmotevasselani'


from lib.map_components.map import Map
from lib.utility_functions.state import State


state = State()


map = Map()
state.game_map = map

for i in range(100):
  map.create_map_layout(state, i)