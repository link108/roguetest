from lib import libtcodpy as libtcod

__author__ = 'cmotevasselani'


class BasicMonster:
    #AI for basic monsters
    def take_turn(self, util):
        #a basic monster takes its turn. If you can see it, it can see you
        monster = self.owner
        if libtcod.map_is_in_fov(util.fov_map, monster.x, monster.y):
            #move towards player if far away
            if monster.distance_to(util.player) >= 2:
                monster.move_towards(util.objects, util.game_map, util.player.x, util.player.y)

            #attack if close enough
            elif util.player.fighter.hp > 0:
                monster.fighter.attack(util.player, util.objects, util.status_panel)

