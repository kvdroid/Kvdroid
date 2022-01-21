KvDroid
=========

A re-implementation of android java API in python with easy access to some Android functionality like Notification,
Reading of Contacts, accessing Webview Cookies, etc...

The aim is to provide full access to Android API which can be used together with Python frameworks like:
[kivy](https://github.com/kivy/kivy), [kivymd](https://github.com/kivymd/kivymd), etc... Or as a standalone, in which
Android native UI is created with only python codes.

### Compiling into APK
To compile, kivy [p4a](https://github.com/kivy/python-for-android) or kivy [buildozer](https://github.com/kivy/buildozer) is
required, and bootstrap must be set to `sdl2`
### Dependencies
```sh
Android min-api21
```

### Installation

```
pip install kvdroid

or

pip install https://github.com/kvdroid/Kvdroid/archive/refs/heads/master.zip # master version
# Note: this works on android only, but you can install it on your desktop for code completion assistance
```

### Buildozer Requirement
```
requirement = kvdroid

or

requirement = https://github.com/kvdroid/Kvdroid/archive/refs/heads/master.zip
```

### Usage
To send notification

```python
from kvdroid.jclass.android.graphics import Color
from kvdroid.tools.notification import create_notification
from kvdroid.tools import get_resource

create_notification(
    small_icon=get_resource("drawable").ico_nocenstore,  # app icon
    channel_id="1", title="You have a message",
    text="hi, just wanted to check on you",
    ids=1, channel_name=f"ch1",
    large_icon="assets/image.png",
    expandable=True,
    small_icon_color=Color().rgb(0x00, 0xC8, 0x53),  # 0x00 0xC8 0x53 is same as 00C853
    big_picture="assets/image.png"
)
```
To read Contacts

```python
from kvdroid.tools.contact import get_contact_details

get_contact_details("phone_book") # gets a dictionary of all contact both contact name and phone mumbers
get_contact_details("names") # gets a list of all contact names
get_contact_details("mobile_no") # gets a list of all contact phone numbers
```
To get Android WebView Cookies

```python
from kvdroid.tools.webkit import get_cookies

get_cookies("https://google.login")
```
To detect keyboard height

```python
from kvdroid.tools import keyboard_height

print(keyboard_height())
```
To detect if app is installed from Play Store or not

```python
from kvdroid.tools.appsource import app_source

print(app_source())
```
To get absolute screen size in dp-pixel and detect current orientation

```python
from kvdroid.tools.metrics import Metrics
screen = Metrics()

print(screen.orientation())
print(screen.width_dp())
print(screen.height_px())
print(screen.resolution())
```
To check if device has a data connection.

```python
from kvdroid.tools.network import network_status, wifi_status, mobile_status

print(network_status())  # for both wifi and mobile
print(wifi_status())    # only for wifi
print(mobile_status())    # only for mobile

```
To check if device is  in dark mode or not

```python
from kvdroid.tools.darkmode import dark_mode

print(dark_mode)
```
To get device informations.
Available options are;
```'model','brand','manufacturer','version','sdk','product','base','rom','security','hardware','tags','sdk_int','total_mem','used_mem','avail_ram','total_ram','used_ram','bat_level','bat_capacity','bat_temperature','bat_voltage','bat_technology'```

```python
from kvdroid.tools.deviceinfo import device_info

print(device_info("model"))
print(device_info("avail_ram", convert=True))
```
To enable immersive mode

```python
from kvdroid.tools import immersive_mode

immersive_mode()
```
To launch a specific app outside your app Activity

```python
from kvdroid.tools import launch_app_externally

launch_app_externally("< app_package >")
```
To launch a specific app within your app Activity

```python
from kvdroid.tools import launch_app_internally

launch_app_internally("< app_package >", "< app_activity >")
```
To open target app's details page

```python
from kvdroid.tools import app_details

app_details("< app_package >")
```
To detect current device's language

```python
from kvdroid.tools.lang import device_lang

print(device_lang())    # en
print(device_lang("DisplayLanguage"))    # English
print(device_lang(option = "DisplayLanguage", display_lang = "fr"))     # Anglais

"""
Available options are ;

Language           ---> en      
ISO3Language       ---> eng 
Country            ---> US 
ISO3Country        ---> USA 
DisplayCountry     ---> United States 
DisplayName        ---> English (United States) 
String             ---> en_US
DisplayLanguage    ---> English
LanguageTag        ---> en-US
"""
```
To set statusbar color

```python
from kvdroid.tools import change_statusbar_color

change_statusbar_color("#FFFFFF", "black")
```
To set navigationbar color

```python
from kvdroid.tools import navbar_color

navbar_color("#FFFFFF")
```
To display a toast message

```python
from kvdroid.tools import toast

toast("hello world")
```
To get absolute sdcard path

```python
from kvdroid.tools.path import sdcard

print(sdcard)
```
To get absolute external_sdcard

```python
from kvdroid.tools.path import external_sdcard

print(external_sdcard)
```
To get path of working app folder

```python
from kvdroid.tools.path import app_folder

print(app_folder)

```
To get file mime Type

```python
from kvdroid.tools import mime_type

mime_type = mime_type("path/to/file")
print(mime_type)
```

To change default wallpaper

```python
from kvdroid.tools import set_wallpaper

set_wallpaper("/sdcard/test.jpg")
```
To use text-to-speech

```python
from kvdroid.tools import speech

speech("hello world", "en")
```
To use default Download Manager

```python
from kvdroid.tools import download_manager

download_manager("< title >", "< description >", "< URL >", "< path >", "< file >")
```
To restart the app

```python
from kvdroid.tools import restart_app

restart_app()
```
To share text via Android Share menu

```python
from kvdroid.tools import share_text

share_text("hello world", title="Share", chooser=False, app_package=None,
           call_playstore=False, error_msg="application unavailable")
```
To share any file via Android Share menu

```python
from kvdroid.tools import share_file

share_file(
    "< path - to - file >", "< title >", "< chooser >", "< app - package: open -with-default - app >",
    "< call_playstore >", "< error_msg >")
share_file("/sdcard/test.pdf", title='Share', chooser=False, app_package=None,
           call_playstore=False, error_msg="application unavailable")
```
To play supported music format or radio stream through Android Media Player
```player.mPLayer = Android Media PLayer```

```python
from kvdroid.tools.audio import Player

player = Player()
player.play("< path - to - music - file >")
player.stream("https://bit.ly/3mHQdzZ")  # radio
player.pause()
player.resume()
player.seek(2) # seconds
player.do_loop(True)  # default is False
player.is_playing()
player.get_duration()
player.current_position()
```
To cast Java Object

```python
from kvdroid.cast import cast_object
from kvdroid.jclass.android import Uri

uri = Uri().fromFile("/home/java/my_document.pdf")
parcelable = cast_object("parcelable", uri)

# Above code  is same as below code::

from kvdroid.jclass.android import Uri
from jnius import cast

uri = Uri().fromFile("/home/java/my_document.pdf")
parcelable = cast("android.os.Parcelabel", uri)

'''
 the difference is, you dont have to remember the package name, just only the name and 
 you are good to go. This will also be helpful for python devs who do have zero knowledge on java
 
 Note:: 
 not all castable java object are included you can open an issue to include all missing 
 castables
'''
```

To access WebView cookies\
(i.e if you compiled your app with webview bootstrap or have Webview in your app)

```python
from kvdroid.tools.webkit import get_cookies

print(get_cookies("https://google.com"))
```
To access android package resource folders like:\
- drawble
- layout
- menu
- values
- mipmap
- etc....

```python
from kvdroid.tools import get_resource

drawable = get_resource("drawable")
```
### License
MIT

