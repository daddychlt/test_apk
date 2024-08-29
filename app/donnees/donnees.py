import json
import os


class Enigme:

    def __init__(self, current_theme_index):
        self.current_theme_index = current_theme_index

        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "donnees.json")

        with open(file_path) as f:
            data = json.load(f)
        self.themes = data['themes'][self.current_theme_index]
        self.theme = self.themes['theme']
        self.letters = self.themes['letters']
        self.word = self.themes['word']
        self.hint = self.themes['hint']
