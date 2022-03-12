from kivy import Config
Config.set("kivy", "exit_on_escape", "0")
from kivymd.app import MDApp
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.card import MDCard
from json import loads
from kivy.clock import Clock

font_file = "assets/fonts/avenir_heavy.ttf"


class MD3Card(MDCard, FakeRectangularElevationBehavior):
    pass


class KvDroid(MDApp):
    icon = "assets/image/icon.png"

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
        from android.permissions import Permission, request_permissions  # NOQA
        request_permissions(
            [Permission.READ_EXTERNAL_STORAGE,
             Permission.WRITE_EXTERNAL_STORAGE,
             Permission.CALL_PHONE,
             Permission.CALL_PRIVILEGED,
             Permission.READ_CONTACTS,
             Permission.WRITE_CONTACTS]
        )
        with open("assets/json/widget.json") as json_file:
            widgets: list = loads(json_file.read())
        Clock.schedule_once(lambda *_: self.root.ids.rv.data.extend(widgets), 3)

    @staticmethod
    def execute_code(code):
        exec(code)


KvDroid().run()
