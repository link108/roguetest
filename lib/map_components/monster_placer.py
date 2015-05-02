from lib.random_libs import libtcodpy as libtcod
from lib.constants.map_constants import MapConstants
from lib.utility_functions.util import Util
from lib.utility_functions.object import Object
from lib.characters.fighter import Fighter
from lib.ai.basic_monster import BasicMonster

__author__ = 'cmotevasselani'

class MonsterPlacer:

    @staticmethod
    def place_monsters(state, game_map, room, objects):
        max_monsters_table = [[2, 0], [3, 3], [5, 5]]
        max_monsters = Util.from_dungeon_level(state, max_monsters_table)

        #choose random number of monsters
        monster_chances = {
            MapConstants.ORC: 80,
            MapConstants.TROLL: Util.from_dungeon_level(state, [[15, 3], [30, 5], [60, 7]])
        }
        num_monsters = libtcod.random_get_int(0, 0, max_monsters)
        for i in range(num_monsters):
            #choose random spot for this monster
            x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
            y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)

            if not game_map.is_blocked(objects, x, y):
                choice = Util.random_choice(monster_chances)
                if choice == MapConstants.ORC:
                    #create an orc
                    fighter_component = Fighter(hp=20, defense=0, power=4, xp=35, score=3)
                    ai_component = BasicMonster()
                    monster = Object(x, y, 'o', MapConstants.ORC,  libtcod.desaturated_green, blocks=True,
                                     fighter=fighter_component, ai=ai_component)
                elif choice == MapConstants.TROLL:
                    #Create a troll
                    fighter_component = Fighter(hp=30, defense=2, power=8, xp=100, score=5)
                    ai_component = BasicMonster()
                    monster = Object(x, y, 'T', MapConstants.TROLL, libtcod.darker_green, blocks=True,
                                     fighter=fighter_component, ai=ai_component)
                objects.append(monster)

