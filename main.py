from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from app.screens.accueil.accueil import AccueilScreen
from app.screens.game.game import GameScreen
from app.screens.starting.starting import StartingScreen


class MyApp(MDApp):
    def build(self):

        self.screenmanager = MDScreenManager()
        self.screenmanager.add_widget(StartingScreen(name="starting"))
        self.screenmanager.add_widget(AccueilScreen(name="accueil"))
        self.screenmanager.add_widget(GameScreen(name="game"))

        return self.screenmanager


if __name__ == '__main__':
    MyApp().run()
