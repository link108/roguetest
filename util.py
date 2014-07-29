__author__ = 'cmotevasselani'

import libtcodpy as libtcod

class Util:

    def __init__(self):
        pass

    @staticmethod
    def player_move_or_attack(player, objects, game_map, dx, dy):
        global fov_recompute

        #the coordinates the player is moving to/attacking
        x = player.x + dx
        y = player.y + dy

        #try tofind an attackable target
        target = None
        for object in objects:
            if object.fighter and object.x == x and object.y == y:
                target = object
                break

        #attack if target found, move otherwise
        if target is not None:
            player.fighter.attack(target, objects)
        else:
            player.move(objects, game_map, dx, dy)
            fov_recompute = True

    @staticmethod
    def handle_keys(player, objects, game_state, game_map):
        global fov_recompute

        #key = libtcod.console_check_for_keypress()    #real-time
        key = libtcod.console_wait_for_keypress(True)
        if key.pressed == False:            #to prevent actions from being preformed twice
            return 'didnt-take-turn'

        if key.vk == libtcod.KEY_ENTER and key.lalt:        # Toggle fullscreen
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        elif key.vk == libtcod.KEY_ESCAPE:                  # exit game
            return 'exit'

        if game_state == 'playing':
            #movement keys
            if key.vk == libtcod.KEY_CHAR:
                if key.c == ord('k'):
                    Util.player_move_or_attack(player, objects, game_map,  0, -1)
                elif key.c == ord('j'):
                    Util.player_move_or_attack(player, objects, game_map, 0, 1)
                elif key.c == ord('h'):
                    Util.player_move_or_attack(player, objects, game_map, -1, 0)
                elif key.c == ord('l'):
                    Util.player_move_or_attack(player, objects, game_map, 1, 0)
                else:
                    return 'didnt-take-turn'



    @staticmethod
    def player_death(player, objects):
        #the game ended, yasd?
        global game_state
        print 'You died!'
        game_state = 'dead'

        #player is a corpse
        player.char = '%'
        player.color = libtcod.dark_red

    @staticmethod
    def monster_death(monster, objects):
        #monster turns into a corpse, does not block, cant be attacked, does not move
        print monster.name.capitalize() + ' is dead!'
        monster.char = '%'
        monster.color = libtcod.dark_red
        monster.blocks = False
        monster.fighter = None
        monster.ai = None
        monster.name = 'remains of ' + monster.name
        monster.send_to_back(objects)
