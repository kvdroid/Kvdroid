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

import os
from kvdroid.tools.iso import iso_codes
from kivy.core.text import LabelBase
from kvdroid.tools.lang import device_lang
from kivy.utils import platform
import xml.etree.ElementTree as ET

FONT_PATH = os.path.join("/", "system", "fonts/")
FONT_XML_PATHS = [os.path.join("/", "system", "etc", "fonts.xml"), os.path.join("/", "system", "etc", "system_fonts.xml")]
FONT_DICT = {}

def system_font(language=None):
    if not language:
        language = device_lang()
    else:
        language = language.split("-")[0]
    if language.lower() in iso_codes.keys():
        if iso_codes[language.lower()] in FONT_DICT.keys():
            return FONT_DICT[iso_codes[language.lower()]]
        else:
            return "Roboto"
    else:
        raise ValueError(
            "The language definition must be in iso639-1 or iso639-2 code formats such as 'en' or 'eng'")

def is_font_exist(font):
    if os.path.isfile(os.path.join(FONT_PATH, font)):
        return font
        
def register_font(lang, name, font):
    if not lang in FONT_DICT.keys():
        LabelBase.register(name= name,
                            fn_regular=FONT_PATH + font,
                            fn_bold= None,
                            fn_italic= None,
                            fn_bolditalic= None)
        FONT_DICT[lang] = name

if platform == "android":
    for font_xml_path in FONT_XML_PATHS:
        if os.path.exists(font_xml_path):
            tree = ET.parse(font_xml_path)
            root = tree.getroot()
            lang_families = [item for item in root.findall("family") if item and 'lang' in item.attrib]
            for family in lang_families:
                font_elements = family.findall("font")
                if font_elements:
                    font_name = font_elements[0].text.strip()
                    if is_font_exist(font_name):
                        name = font_name.split(".")[0].split("-")[0]
                        lang_code = family.attrib["lang"].split(",")
                        if len(lang_code) >= 2:
                            for lang in lang_code:
                                lang_code = lang.split("-")[-1].strip()
                                register_font(lang_code,name,font_name)
                        else:
                            if lang_code[0] == "ja":
                                lang_code = "Jpan"
                            elif lang_code[0] == "ko":
                                lang_code = "Kore"
                            elif lang_code[0] == "zh":
                                lang_code = "Hant"
                            else:
                                lang_code = lang_code[0].split("-")[-1].strip()
                            register_font(lang_code,name,font_name)

                        
#print(system_font("ar"))
