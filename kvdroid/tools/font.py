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
                        "font_name": system_font(locale.getLanguage())}
                if system_font(locale.getLanguage()) != "Roboto" and not item in self.ids.rclist.data:
                    self.ids.rclist.data.append(item)
            except:
                print(locale.getLanguage(), locale.getDisplayLanguage())


class Test(App):
    def build(self):
        return MainApp()


Test().run()
"""


import re
import os
from kvdroid.tools.iso import iso_codes
from kivy.core.text import LabelBase
from kvdroid.tools.lang import device_lang

def system_font(language=None):
    if language != None:
        if language.lower() in iso_codes.keys():
            try:
                return font_dict[iso_codes[language.lower()]]
            except:
                return "Roboto"
        else:
            raise ValueError(
                "The language definition must be in iso639-1 or iso639-2 code formats such as 'en' or 'eng'")
    else:
        locale = device_lang()
        try:
            return font_dict[iso_codes[locale]]
        except:
            return "Roboto"


def register_font(lang, font):
    if not lang in font_dict.keys():
        font_dict[lang] = font["name"]
        LabelBase.register(name=font["name"],
                           fn_regular=path + font["regular"],
                           fn_bold=path +
                           font["bold"] if "bold" in font.keys() else None,
                           fn_italic=path +
                           font["italic"] if "italic" in font.keys() else None,
                           fn_bolditalic=path + font["bolditalic"] if "bolditalic" in font.keys() else None)


def is_font_exist(font):
    if os.path.exists(path + font):
        return font
    else:
        new_font = font.split('.')[0]+'.otf'
        if os.path.exists(new_font):
            return new_font
        else:
            return None


def define_font(lang, item):
    temp = {}
    split_item = item.splitlines()
    for f in split_item:
        if f.strip().startswith("<font"):
            font = re.findall(
                "(?<=\">)[A-Z].*\.ttf|(?<=\">)[A-Z].*\.ttc|(?<=\">)[A-Z].*\.otf", f)[0]
            font = is_font_exist(font)
            if font:
                temp["name"] = font.split("-")[0]
                if "-Regular" in font:
                    if not "regular" in temp.keys():
                        temp["regular"] = font
                elif "-Bold" in font:
                    if not "bold" in temp.keys():
                        temp["bold"] = font
                elif "-Italic" in font:
                    if not "italic" in temp.keys():
                        temp["italic"] = font
                elif "-BoldItalic" in font:
                    if not "bolditalic" in font:
                        temp["bolditalic"] = font

        if "regular" in temp.keys():
            register_font(lang, temp)
    temp = {}


path = "/system/fonts/"
font_dict = {}

if os.path.exists("/system/etc/fonts.xml"):
    r = open("/system/etc/fonts.xml").read()
elif os.path.exists("/system/etc/system_fonts.xml"):
    r = open("/system/etc/system_fonts.xml").read()
else:
    pass
if r:
    langs = re.findall("<family lang=[\s\S]*?</family>", r)
    if langs:
        for i in langs:
            lang = re.findall("\"(.*?)\"", i)[0]
            split_lang = lang.split()
            for s in split_lang:
                lang = s.split("-")[-1]
                if lang == "ja":
                    lang = "Jpan"
                if lang == "ko":
                    lang = "Kore"
                if lang == 'Hans':
                   define_font('Hant',i)
                define_font(lang, i)
