__author__ = 'cmotevasselani'

from lib.map_components.monster_placer import MonsterPlacer
from lib.map_components.item_placer import ItemPlacer


class MapUtils:
  @staticmethod
  def place_objects(state, game_map, room, objects):
    MonsterPlacer.place_monsters(state, game_map, room, objects)
    ItemPlacer.place_items(state, game_map, room, objects)


