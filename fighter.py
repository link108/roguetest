__author__ = 'cmotevasselani'

class Fighter:
    #combat related properties and methods (npcs, monsters, player)
    def __init__(self, hp, defense, power, death_function = None):
        self.death_function = death_function
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.death_function = death_function

    def take_damage(self, damage, objects):
        #apply damage if possible
        if damage > 0:
            self.hp -= damage
            if self.hp <= 0:
                function = self.death_function
                if function is not None:
                    function(self.owner, objects)


    def attack(self, target, objects):
        #simple formula for attack damage
        damage = self.power - target.fighter.defense

        if damage > 0:
            #make the target take some damage
            print self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + 'hit points'
            target.fighter.take_damage(damage, objects)
        else:
            print self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!'
