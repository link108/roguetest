__author__ = 'cmotevasselani'


class HighScore:

    def __init__(self, name, score, player_class, player_race, date, turns, level, dungeon_level, message):
        self.name = name
        self.score = score
        self.player_class = player_class
        self.player_race = player_race
        self.date = date
        self.turns = turns
        self.level = level
        self.dungeon_level = dungeon_level
        self.message = message


    def __str__(self):
        to_str = ""
        to_str += "score: " + str(self.score) + " \n"
        to_str += "name: " + str(self.name) + " \n"
        to_str += "class: " + str(self.player_class) + " "
        to_str += "race: " + str(self.player_race) + " "
        to_str += "date: " + str(self.date) + " "
        to_str += "turns: " + str(self.turns) + " "
        to_str += "level: " + str(self.level) + " "
        to_str += "dungeon_level: " + str(self.dungeon_level) + " "
        to_str += "message: " + str(self.message) + " "
        return to_str



