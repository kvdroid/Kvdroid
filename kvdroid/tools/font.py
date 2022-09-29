"""
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview import RecycleView
from kivy.lang import Builder
from kvdroid.jclass.java import Locale

from kvdroid.tools.font import system_font

Builder.load_string(""

<MainApp>:
    RCList:
        id: rclist
        size_hint: 1,1

<RCList>:
    viewclass: 'XBox'
    RecycleBoxLayout:
        spacing:  dp(10)
        #default_size: dp(100), dp(100)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
<XBox>:
    Button:
        text: root.name
        font_size: "22sp"
    Button:
        text: root.native
        font_name: root.font_name
        font_size: "22sp"
        on_press: print(root.font_name)


"")


class XBox(BoxLayout):
    name = StringProperty()
    native = StringProperty()
    font_name = StringProperty()


class RCList(RecycleView):
    def __init__(self, **kwargs):
        super(RCList, self).__init__(**kwargs)
        self.data = []


class MainApp(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for locale in Locale().getAvailableLocales():
            try:
                item = {"name": locale.getDisplayLanguage(Locale("en")),
                        "native": locale.getDisplayLanguage(Locale(locale.getLanguage())),
                        "font_name": system_font('NotoNaskhArabic')['fn_regular']}
                self.ids.rclist.data.append(item)
            except:
                print(locale.getLanguage(), locale.getDisplayLanguage())


class Test(App):
    def build(self):
        return MainApp()


Test().run()
"""


import os.path
from xml.etree.ElementTree import ElementTree

if os.path.exists("/system/etc/fonts.xml"):
    SYSTEM_FONT_PATH = "/system/etc/fonts.xml"
else:
    SYSTEM_FONT_PATH = "/system/etc/system_fonts.xml"


# noinspection PyTypedDict
def get_system_font():
    font_dict = {}
    tree = ElementTree().parse(SYSTEM_FONT_PATH)
    for family in tree.findall("family"):
        for font in family.findall("./"):
            font_basename = font.text.strip()
            if font_basename.split('-')[0] not in font_dict:
                font_dict[font_basename.split('-')[0]] = dict(
                    fn_italic=None,
                    fn_bold=None,
                    fn_bolditalic=None,
                    fn_regular=None,
                    name=font_basename.split('-')[0]
                )
            font_name = font_dict[font_basename.split('-')[0]]
            if font.get("weight") == "400":
                if "italic" in font_basename.lower():
                    font_name["fn_italic"] = f"/system/fonts/{font_basename}"
                else:
                    font_name["fn_regular"] = f"/system/fonts/{font_basename}"

            elif font.get("weight") == "700":
                if "bolditalic" in font_basename.lower():
                    font_name["fn_bolditalic"] = f"/system/fonts/{font_basename}"
                elif "bold" in font_basename.lower():
                    font_name["fn_bold"] = f"/system/fonts/{font_basename}"
    return font_dict


# This only works on apps that makes use of the Kivy GUI Framework
def register_system_font():
    from kivy.core.text import LabelBase
    font_list = get_system_font().values()
    for font_data in font_list:
        LabelBase.register(**font_data)


def system_font(name):
    return get_system_font()[name]

