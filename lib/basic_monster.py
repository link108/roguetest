from lib import libtcodpy as libtcod

__author__ = 'cmotevasselani'


class BasicMonster:
    #AI for basic monsters
    def take_turn(self, fov_map, player, objects, game_map):
        #a basic monster takes its turn. If you can see it, it can see you
        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            #move towards player if far away
            if monster.distance_to(player) >= 2:
                monster.move_towards(objects, game_map, player.x, player.y)

            #attack if close enough
            elif player.fighter.hp > 0:
                monster.fighter.attack(player, objects, game_map.status_panel)

