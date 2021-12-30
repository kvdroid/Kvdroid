from kivy import Config
from kivymd.app import MDApp
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.card import MDCard
from json import loads

Config.set("kivy", "exit_on_escape", "0")
font_file = "assets/fonts/avenir_heavy.ttf"


class MD3Card(MDCard, FakeRectangularElevationBehavior):
    pass


class KvDroid(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "A700"
        self.theme_cls.font_styles.update(
            {
                "H1": [font_file, 96, False, -1.5],
                "H2": [font_file, 60, False, -0.5],
                "H3": [font_file, 48, False, 0],
                "H4": [font_file, 34, False, 0.25],
                "H5": [font_file, 24, False, 0],
                "H6": [font_file, 20, False, 0.15],
                "Button": [font_file, 14, True, 1.25],
                "Body1": [font_file, 16, False, 0.5],
                "Body2": [font_file, 14, False, 0.25]
            }
        )

    def on_start(self):
        print(self.root)


KvDroid().run()
