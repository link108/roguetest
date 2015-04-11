__author__ = 'cmotevasselani'

from lib.constants.constants import Constants
from lib.constants.map_constants import MapConstants
from lib.high_scores.high_score import HighScore
import shelve
import os.path
import datetime

class HighScores:

    def __init__(self):
        self.high_scores = []
        if not os.path.isfile(Constants.HIGH_SCORE_FILE):
            self.save_high_scores()
        self.load_high_scores()

    def load_high_scores(self):
        file = shelve.open(Constants.HIGH_SCORE_FILE, 'r')
        self.high_scores = file['high_scores']
        file.close()

    def save_high_scores(self):
        file = shelve.open(Constants.HIGH_SCORE_FILE, 'n')
        file['high_scores'] = self.get_high_scores()
        file.close()

    def get_high_scores(self):
        return sorted(self.high_scores, key=lambda high_score: high_score.score)[:26]

    def show_high_scores(self, state, menu):
        high_scores = self.get_high_scores()
        high_scores_to_display = map(HighScore.to_quick_str, high_scores)
        index = menu.display_menu_return_index('High Score list', high_scores_to_display, MapConstants.MAP_WIDTH, state.con, override_height=MapConstants.MENU_HEIGHT_ADDITION)
        if index:
            chosen_high_score = high_scores[index]
            menu.display_menu_return_index('High Score of ' + chosen_high_score.name, [str(chosen_high_score)], MapConstants.MAP_WIDTH, state.con, override_height=20, option_char=False)


    def add_high_score(self, state):
        score_to_add = HighScore(
            state.player.name,
            state.score,
            state.player_class,
            state.player_race,
            datetime.datetime.now().strftime("%y-%m-%d-%H:%M:%S"),
            state.turn,
            state.player.level,
            state.dungeon_level,
            "you died!"
        )
        self.high_scores.append(score_to_add)
        self.save_high_scores()





