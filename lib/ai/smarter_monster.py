from lib.random_libs import libtcodpy as libtcod

__author__ = 'cmotevasselani'


class SmarterMonster:
  # AI for basic monsters
  def take_turn(self, state):
    # a basic monster takes its turn. If you can see it, it can see you
    monster = self.owner
    if libtcod.map_is_in_fov(state.fov_map, monster.x, monster.y):
      # move towards player if far away
      if monster.fighter.hp < monster.fighter.base_max_hp * .25:
        monster.move_away_from_player(state)
      elif monster.distance_to(state.player) >= 2:
        monster.move_towards(state.objects, state.game_map, state.player.x, state.player.y)

      # attack if close enough
      elif state.player.fighter.hp > 0:
        monster.fighter.attack(state.player, state)

