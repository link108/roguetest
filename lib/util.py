from lib import libtcodpy as libtcod

__author__ = 'cmotevasselani'


class Util:

    def __init__(self, status_panel):
        self.status_panel = status_panel

    @staticmethod
    def player_move_or_attack(player, objects, game_map, dx, dy, status_panel):
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
            player.fighter.attack(target, objects, status_panel)
        else:
            player.move(objects, game_map, dx, dy)
            fov_recompute = True

    @staticmethod
    def handle_keys(player, objects, game_state, game_map, status_panel, inventory):
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
                    Util.player_move_or_attack(player, objects, game_map,  0, -1, status_panel)
                elif key.c == ord('j'):
                    Util.player_move_or_attack(player, objects, game_map, 0, 1, status_panel)
                elif key.c == ord('h'):
                    Util.player_move_or_attack(player, objects, game_map, -1, 0, status_panel)
                elif key.c == ord('l'):
                    Util.player_move_or_attack(player, objects, game_map, 1, 0, status_panel)
                elif key.c == ord('y'):
                    Util.player_move_or_attack(player, objects, game_map, -1, -1, status_panel)
                elif key.c == ord('u'):
                    Util.player_move_or_attack(player, objects, game_map, 1, -1, status_panel)
                elif key.c == ord('b'):
                    Util.player_move_or_attack(player, objects, game_map, -1, 1, status_panel)
                elif key.c == ord('n'):
                    Util.player_move_or_attack(player, objects, game_map, 1, 1, status_panel)
                elif key.c == ord('g'):
                    #pick up an item
                    for object in objects:  #look for an item in the player's tile
                        if object.x == player.x and object.y == player.y and object.item:
                            object.item.pick_up(inventory)
                            break
                else:
                    return 'didnt-take-turn'

    @staticmethod
    def player_death(player, objects, status_panel):
        #the game ended, yasd?
        # global game_state
        status_panel.message( 'You died!', libtcod.white)
        game_state = 'dead'

        #player is a corpse
        player.char = '%'
        player.color = libtcod.dark_red

    @staticmethod
    def monster_death(monster, objects, status_panel):
        #monster turns into a corpse, does not block, cant be attacked, does not move
        status_panel.message( monster.name.capitalize() + ' is dead!', libtcod.white)
        monster.char = '%'
        monster.color = libtcod.dark_red
        monster.blocks = False
        monster.fighter = None
        monster.ai = None
        monster.name = 'remains of ' + monster.name
        monster.send_to_back(objects)
