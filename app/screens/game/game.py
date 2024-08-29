import json
import os

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.button import Button
from kivymd.uix.behaviors import MagicBehavior
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from nltk import edit_distance

from app.donnees import donnees as dn

KV = """
<MagicButton@MagicBehavior+MDRaisedButton>:


<GameScreen>:

    MDBoxLayout:
        id: grid
        opacity: 1
        orientation: "vertical"

        MDTopAppBar:
            title: "Jedemo"
            anchor_title: "left"
            opposite_color: True
            left_action_items: [["arrow-left", lambda x: root.go_to_home(self)]]

        MDProgressBar:
            id: progress
            type: "determinate"
            color: "white"
            size_hint: None, None
            height: "2dp"
            width: self.parent.width

        MDBoxLayout:
            orientation: "vertical"

            MDBoxLayout:
                id: box_level
                orientation: "vertical"
                size_hint: 1, None

                MDLabel:
                    id: level
                    halign: "center"
                    md_bg_color: "#e1dedd"

            MDBoxLayout:
                orientation: "vertical"

                MDBoxLayout:
                    orientation: "vertical"

                    MDBoxLayout:
                        size_hint_y: None
                        height: "150dp"

                        MDLabel:
                            id: indice
                            halign: "center"
                            font_size:"15dp"

                    MDLabel:
                        id: texte
                        text: "_"
                        halign: "center"
                        font_size:"20dp"

                MDGridLayout:
                    cols: 3
                    size_hint: None, None
                    size: "146dp", "55dp"
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}

                    MDIconButton:
                        icon: "delete"
                        theme_icon_color: "Custom"
                        icon_color: "red"
                        ripple_alpha: 0
                        on_release: root.delete_word(self)

                    MDIconButton:
                        icon: "backspace"
                        theme_icon_color: "Custom"
                        icon_color: "red"
                        ripple_alpha: 0
                        on_release: root.erase_letter(self)

                    MDIconButton:
                        id: check
                        icon: "check"
                        theme_icon_color: "Custom"
                        icon_color: "green"
                        ripple_alpha: 0
                        on_release: root.validate_word(self)





        MDBoxLayout:
            orientation: "vertical"
            size_hint: None, None
            width: self.parent.width
            height: "200dp"

            MDGridLayout:
                id: bouton_box
                rows: 2
                size_hint: .9, None
                height: "100dp"
                spacing: "10dp"
                pos_hint: {"center_x": 0.5, "center_y": 0.5}

            MDWidget:
                size_hint_y: None
                height: "10dp"

            MDLabel:
                id: prox
                halign: "center"
                color: "red"
                font_size:"15dp"
                opacity: 0

            MDWidget:
                size_hint_y: None
                height: "70dp"

    MDFloatLayout:
        id: recompense
        size_hint: None, None
        size: "200dp", "250dp"
        radius: [45]
        md_bg_color: "red"
        opacity: .8
        elevation: 5
        line_color: "blue"
        line_width: 2
        pos_hint: {"center_x": 0.5, "center_y":1.5}

        MDLabel:
            id: loadingText
            text: "Bravo, bien joué..."
            halign: "center"
            font_size: "20dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.8}

        MDIcon:
            id: center_crown
            icon: "crown"
            font_size: "50dp"
            theme_text_color: "Custom"
            text_color: "yellow"
            pos_hint: {"center_x": .5, "center_y": .5}

        MDIcon:
            id: left_crown
            icon: "crown"
            font_size: "40dp"
            theme_text_color: "Custom"
            text_color: "yellow"
            pos_hint: {"center_x": .5, "center_y": .5}

        MDIcon:
            id: right_crown
            icon: "crown"
            font_size: "40dp"
            theme_text_color: "Custom"
            text_color: "yellow"
            pos_hint: {"center_x": .5, "center_y": .5}

        MagicButton:
            id: bouton_next_level
            text: "Continuer"
            size_hint: .4, None
            pos_hint: {"center_x":.5, "center_y":.3}
            on_release: root.next_theme(self)
            on_press: self.grow()

        MDProgressBar:
            id: progress_rep
            type: "determinate"
            color: "blue"
            back_color: "white"
            size_hint: None, None
            height: "2dp"
            width: "100dp"
            pos_hint: {"center_x":.5, "center_y":.1}
            opacity: 0
"""

Builder.load_string(KV)


class MagicButton(MagicBehavior, MDRaisedButton):
    pass


class GameScreen(MDScreen):

    global liste_reperage_boutns

    liste_reperage_boutns = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.recompense = False
        self.current_theme_index = 0
        self.enigme = dn.Enigme(self.current_theme_index)
        self.game()

    # fonction de chargement
    def game(self):
        # Charger le thème courant
        themes = self.get_themes()

        # Vérifier si nous avons encore des thèmes à parcourir
        if self.current_theme_index < len(themes):

            self.enigme = dn.Enigme(self.current_theme_index)  # Charger le nouvel enigme

            self.ids.progress.value = self.ids.progress.value + 5   # Afficher le thème
            self.ids.level.text = self.enigme.theme  # Afficher le thème
            self.ids.indice.text = self.enigme.hint  # Afficher l'indice
            self.ids.texte.text = "_"  # Réinitialiser le texte affiché

            # Réinitialiser les boutons
            self.ids.bouton_box.clear_widgets()
            for letter in self.enigme.letters:
                button = Button(text=letter.upper(), on_release=self.display_letter)
                button.disabled = False
                self.ids.bouton_box.add_widget(button)

        else:
            # Si nous avons parcouru tous les thèmes, finir le jeu ou recommencer
            self.go_to_end()



    def display_letter(self, instance):
        if not self.recompense:
            current_text = self.ids.texte.text
            if current_text.endswith("_"):
                current_text = current_text[:-1]  # Remove the underscore if it's at the end
            self.ids.texte.text = current_text + instance.text + "_"
            instance.disabled = True
            liste_reperage_boutns.append(instance)

    def erase_letter(self, instance):
        if not self.recompense:
            current_text = self.ids.texte.text
            if current_text.endswith("_"):
                current_text = current_text[:-1]  # Remove the underscore if it's at the end
            if len(current_text) > 0:
                self.ids.texte.text = current_text[:-1] + "_"
            if len(liste_reperage_boutns) > 0:
                bouton = liste_reperage_boutns[len(liste_reperage_boutns)-1]
                bouton.disabled = False
                liste_reperage_boutns.remove(bouton)

    def delete_word(self, instance):
        if not self.recompense:
            for bouton in liste_reperage_boutns:
                bouton.disabled = False
            liste_reperage_boutns.clear()

            self.ids.texte.text = "_"

    def verifier_proximite(self, mot_ecrit, mot_a_deviner):
        seuil = 2  # Seuil de distance pour considérer les mots comme proches
        distance = edit_distance(mot_ecrit, mot_a_deviner)

        if distance <= seuil:
            self.ids.prox.text = "Vous êtes proche"
        else:
            self.ids.prox.text = "Essayer encore"
        (Animation(opacity=1, duration=1) + Animation(opacity=0, duration=1)).start(self.ids.prox)

    def validate_word(self, instance):
        if not self.recompense:
            current_text = self.ids.texte.text
            if len(current_text) > 1:
                if current_text[:-1] == self.enigme.word:
                    self.ids.texte.text = current_text[:-1]
                    self.ids.texte.color = "green"
                    Clock.schedule_once(self.recompense_come, 1)  # Planifier la restauration après 5 secondes

                else:
                    self.ids.texte.color = "red"
                    self.verifier_proximite(current_text, self.enigme.word)
                    self.ids.texte.text = current_text[:-1]  # Enlever la dernière lettre
                    Clock.schedule_once(self.restore_text, 1)  # Planifier la restauration après 5 secondes


    def restore_text(self, dt):
        self.ids.texte.color = "black"  # Remettre la couleur originale, ajustez si nécessaire
        current_text = self.ids.texte.text
        self.ids.texte.text = current_text + "_"  # Ajouter un curseur à la fin du texte

    def next_theme(self, instance):
        self.recompense_back(instance)
        self.ids.texte.color = "black"  # Remettre la couleur originale
        self.ids.texte.text = "_"

        self.current_theme_index += 1

        # Charger le prochain mot/thème
        self.game()

    def get_themes(self):
        base_dir = os.path.dirname(os.path.abspath("app/donnees/donnees.py"))
        file_path = os.path.join(base_dir, "donnees.json")
        with open(file_path) as f:
            data = json.load(f)
        return data['themes']

    def recompense_come(self, instance):
        self.recompense = True
        self.ids.grid.opacity = .5
        liste_reperage_boutns.clear()
        (Animation(pos_hint={"center_y": 0.5}, duration=0.2) + Animation(size=[dp(250), dp(100)], duration=0.2) + Animation( size=[dp(200), dp(250)], duration=0.2)).start(self.ids.recompense)
        Animation(pos_hint={"center_y": 0.6}, duration=0.3).start(self.ids.center_crown)
        Animation(pos_hint={"center_x": 0.3, "center_y": .55}, duration=0.3).start(self.ids.left_crown)
        Animation(pos_hint={"center_x": 0.7, "center_y": .55}, duration=0.3).start(self.ids.right_crown)
        Clock.schedule_once(self.start_progress, 1)

    def start_progress(self, dt):
        # Augmenter la valeur cible
        target_value = min(self.ids.progress_rep.value + 5, 100)  # S'assurer que la valeur ne dépasse pas 100

        self.ids.progress_rep.opacity = 1
        # Animation fluide pour passer de la valeur actuelle à la valeur cible
        animation = Animation(value=target_value, duration=1)  # Ajuster la durée pour plus de fluidité
        animation.start(self.ids.progress_rep)

    def recompense_back(self, instance):
        self.ids.grid.opacity = 1
        self.recompense = False
        self.ids.progress_rep.opacity = 0
        Animation(pos_hint={"center_y": 1.5}, duration=0.2).start(self.ids.recompense)


    def go_to_home(self, instance):
        self.manager.current = 'accueil'