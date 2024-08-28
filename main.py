from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from app.screens.accueil.accueil import AccueilScreen


class MyApp(MDApp):
    def build(self):

        self.screenmanager = MDScreenManager()
        self.screenmanager.add_widget(AccueilScreen(name="accueil"))

        return self.screenmanager


if __name__ == '__main__':
    MyApp().run()
