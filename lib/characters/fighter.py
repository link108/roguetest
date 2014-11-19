from lib.random_libs import libtcodpy as libtcod

__author__ = 'cmotevasselani'


class Fighter:
    #combat related properties and methods (npcs, monsters, player)
    def __init__(self, hp, defense, power, xp, death_function=None):
        self.level = 1
        self.max_hp = hp
        self.xp = xp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.death_function = death_function

    def take_damage(self, damage, state):
        #apply damage if possible
        if damage > 0:
            self.hp -= damage
            if self.hp <= 0:
                function = self.death_function
                if function is not None:
                    function(self.owner, state)
                if self.owner != state.player:
                    state.player.fighter.xp += self.xp


    def attack(self, target, state):
        #simple formula for attack damage
        damage = self.power - target.fighter.defense

        if damage > 0:
            #make the target take some damage
            state.status_panel.message(self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points', libtcod.white)
            target.fighter.take_damage(damage, state)
        else:
            state.status_panel.message(self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!', libtcod.gray)

    def heal(self, amount):
        self.hp += amount
        # dont go over max hp limit
        if self.hp > self.max_hp:
            self.hp = self.max_hp
