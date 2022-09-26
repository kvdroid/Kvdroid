import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"
from kivy import Config

Config.set("kivy", "exit_on_escape", "0")
from kivy.uix.behaviors import ButtonBehavior
from behavior import BackgroundLineBehavior
from kivy.uix.label import Label
from kivy.app import App
from kivy.clock import Clock
from tools import kvdroid_tools
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy import platform


class LineButton(ButtonBehavior, BackgroundLineBehavior, Label):
    pass


class KvDroid(App):
    icon = "assets/image/icon.png"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = get_color_from_hex("#FAFAFA")

    def on_start(self):
        if platform == "android":
            from android.permissions import Permission, request_permissions  # NOQA
            request_permissions(
                [Permission.READ_EXTERNAL_STORAGE,
                 Permission.WRITE_EXTERNAL_STORAGE,
                 Permission.CALL_PHONE,
                 Permission.CALL_PRIVILEGED,
                 Permission.READ_CONTACTS,
                 Permission.WRITE_CONTACTS,
                 Permission.READ_SMS]
            )
        Clock.schedule_once(lambda *_: self.root.ids.rv.data.extend(kvdroid_tools), 3)

    @staticmethod
    def execute_code(code):
        exec(code)


KvDroid().run()
