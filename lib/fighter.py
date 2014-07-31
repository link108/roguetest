__author__ = 'cmotevasselani'

from lib import libtcodpy as libtcod


class Fighter:
    #combat related properties and methods (npcs, monsters, player)
    def __init__(self, hp, defense, power, death_function = None):
        self.death_function = death_function
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.death_function = death_function

    def take_damage(self, damage, objects, status_panel):
        #apply damage if possible
        if damage > 0:
            self.hp -= damage
            if self.hp <= 0:
                function = self.death_function
                if function is not None:
                    function(self.owner, objects, status_panel)


    def attack(self, target, objects, status_panel):
        #simple formula for attack damage
        damage = self.power - target.fighter.defense

        if damage > 0:
            #make the target take some damage
            status_panel.message(self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points', libtcod.white)
            target.fighter.take_damage(damage, objects, status_panel)
        else:
            status_panel.message(self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!', libtcod.gray)
