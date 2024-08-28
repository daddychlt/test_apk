from kivy.animation import Animation
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen


KV = """
<MagicButton@MagicBehavior+MDRaisedButton>:

<AccueilScreen>:
    name: "accueil"

    MDBoxLayout:
        orientation: "vertical"

        MDBoxLayout:
            orientation: "vertical"

            MDWidget:
                size_hint_y: None
                height: "100dp"

            MDLabel:
                id: jedemo_label
                text: "Jedemo"
                halign: "center"
                font_size: "50"

        MDBoxLayout:
            orientation: "vertical"
            spacing: "20dp"

            MagicButton:
                text: "Jouer"
                size_hint: .4, None
                pos_hint: {"center_x":.5}
                #on_release: root.go_to_game(self)
                on_press: self.grow()

            MDWidget:
                size_hint_y: None
                height: "150dp"
"""

Builder.load_string(KV)

class AccueilScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.jedemo_label.bind(on_touch_down=self.animate_label)

    def animate_label(self, instance, touch):
        if self.ids.jedemo_label.collide_point(*touch.pos):
            animation = Animation(font_size=70, duration=0.5) + Animation(font_size=50, duration=0.5)
            animation.start(self.ids.jedemo_label)
