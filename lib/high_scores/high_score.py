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

  def to_quick_str(self):
    to_str = ""
    to_str += "Score: " + str(self.score) + ", "
    to_str += "Name: " + str(self.name) + ", "
    to_str += "Class: " + str(self.player_class) + ", "
    to_str += "Race: " + str(self.player_race) + " "
    return to_str

  def __str__(self):
    to_str = "\n"
    to_str += "Score: " + str(self.score) + " \n\n"
    to_str += "Name: " + str(self.name) + " \n\n"
    to_str += "Class: " + str(self.player_class) + " \n\n"
    to_str += "Race: " + str(self.player_race) + " \n\n"
    to_str += "Date: " + str(self.date) + " \n\n"
    to_str += "Turns: " + str(self.turns) + " \n\n"
    to_str += "Level: " + str(self.level) + " \n\n"
    to_str += "Dungeon Level: " + str(self.dungeon_level) + " \n\n"
    to_str += "Message: " + str(self.message) + " \n\n"
    return to_str



