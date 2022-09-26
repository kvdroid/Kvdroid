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

To use system-provided fonts

:warning: `That function is so experimental. It should work for Android 7 and above but not been tested on much devices. It is actually for multilingual purposes to use system-provided fonts for no Latin languages. system_font() will always return the supported font from /system/fonts for the current device language.  Also, you could use any language-supported font from the system just by calling the system_font function with the target language's iso639-1 or iso639-2 abbreviation such as font_name = system_font('zh') or system_font('zho'). `

```python
from kivy.uix.label import Label
from kvdroid.tools.font import system_font

# that will return the default font for the device's current language.
Label(text = "example", font_name = system_font())

# for the specific language font
Label(text = "你好世界", font_name = system_font('zho')) # Language definition must be iso639-1 or iso639-2 abbreviation.  https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
```

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

To get a list of all installed packages (Applications)

```python
from kvdroid.tools.package import all_packages

print(all_packages())

"""
['com.google.android.carriersetup',
 'com.android.cts.priv.ctsshim',
 'com.google.android.ext.services',
 'com.android.providers.telephony',
 'com.android.providers.calendar'...]
"""
```

To get all main activities

```python
from kvdroid.tools.package import all_main_activities

print(all_main_activities())

"""
[{'com.android.settings': 'com.android.settings.Settings'},
 {'com.android.vending': 'com.android.vending.AssetBrowserActivity'},
 {'com.google.android.contacts': 'com.android.contacts.activities.PeopleActivity'},
 {'com.google.android.deskclock': 'com.android.deskclock.DeskClock'}...]
"""
```

To check if the package is a system application

```python
from kvdroid.tools.package import is_system_package

print(is_system_package("com.android.settings"))
```

To check if the package is enabled

```python
from kvdroid.tools.package import is_package_enabled

print(is_package_enabled("com.android.settings"))
```

To get a specific app details

```python
from kvdroid.tools.package import package_info

print(package_info("com.android.settings"))

"""
{'activities': ['org.chromium.settings.SettingsBlackHoleActivity',
                'com.android.settings.Settings$NetworkDashboardActivity',
                'com.android.settings.network.NetworkSettings',
                'com.android.settings.Settings$AdvancedAppsActivity',
                'com.android.settings.app.AdvancedAppsSettings'...],
 'dataDir': '/data/user_de/0/com.android.settings',
 'loadIcon': <android.graphics.drawable.Drawable at 0x7e8e15bac8b0 jclass=android/graphics/drawable/Drawable jself=<LocalRef obj=0x6196 at 0x7e8e15f63e30>>,
 'loadLabel': 'Settings',
 'packageName': 'com.android.settings',
 'permissions': ['org.chromium.settings.ENABLE_INPUT_METHOD',
                 'android.permission.REQUEST_NETWORK_SCORES',
                 'android.permission.WRITE_MEDIA_STORAGE',
                 'android.permission.WRITE_EXTERNAL_STORAGE'...],
 'processName': 'com.android.settings',
 'publicSourceDir': '/system/priv-app/ArcSettings/ArcSettings.apk',
 'sharedLibraryFiles': None,
 'sourceDir': '/system/priv-app/ArcSettings/ArcSettings.apk'}
"""
```
 
To get an activity info

```python
from kvdroid.tools.package import activity_info

print(activity_info("com.android.settings","com.android.settings.network.NetworkSettings"))

"""
{'loadIcon': <android.graphics.drawable.Drawable at 0x7e8e15c46db0 jclass=android/graphics/drawable/Drawable jself=<LocalRef obj=0x6156 at 0x7e8e15c8c8b0>>,
 'loadLabel': 'Network and Internet'}
"""
```
 
To save a drawable object to given path as png

```python
from kvdroid.tools.package import package_info
from kvdroid.tools.graphics import save_drawable

app = package_info("com.android.settings")
app_icon = app["loadIcon"]

# <android.graphics.drawable.Drawable at 0x7e8e15c46db0 jclass=android/graphics/drawable/Drawable jself=<LocalRef obj=0x6156 at 0x7e8e15c8c8b0>>

save_drawable(app_icon, "< path >", "< file_name >")

# That will save the app icon to given path and return the path + filename
# can be used like

from kivy.uix.image import Image

Image(source=save_drawable(app_icon, "< path >", "< file_name >"))
```


To check if the given app is installed from PlayStore

```python
from kvdroid.tools.package import package_source

print(package_source("< package_name >"))
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
To launch an application

```python
from kvdroid.tools import launch_app

launch_app("< app_package >")
```
To launch a specific application activity

```python
from kvdroid.tools import launch_app_activity

launch_app_activity("< app_package >", "< app_activity >")
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

To get a list of supported languages on the device

```python
from kvdroid.tools.lang import supported_languages
print(supported_languages())

"""
['af', 'agq', 'ak', 'am', 'ar', 'as', 'asa', 'ast'...]
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
To access android package resource folders like:
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
To get Wi-Fi IP Address
```python
from kvdroid.tools.network import get_wifi_ip_address
print(get_wifi_ip_address())
```
To send email
```python
from kvdroid.tools.email import send_email
send_email(
    recipient=["test@gmail.com"], 
    subject="Hello there", 
    body="This is kvdroid"
)
```
To send an email with an attachment (androidx is required). \
Also note before you can share files on Android version greater \
than 10, you must specify a provider in the AndroidManifest.xml \
inside the \<application> tag e.g
```xml
<provider
    android:name="androidx.core.content.FileProvider"
    android:authorities="${applicationId}.fileprovider"
    android:grantUriPermissions="true"
    android:exported="false">
    <meta-data
        android:name="android.support.FILE_PROVIDER_PATHS"
        android:resource="@xml/filepath" />
</provider>
```
and also specify file path in the res/xml/filepath.xml of the android project folder e.g
```xml
<paths>
    <files-path name="document" path="app" />
</paths>
```
refer to [android developer FileProvder Documentation](https://developer.android.com/reference/androidx/core/content/FileProvider) to know more
```python
from kvdroid.tools.email import send_email
from os import getenv
from os.path import join
send_email(
    recipient=["test@gmail.com"], 
    subject="Hello there", 
    body="This is kvdroid",
    file_path=join(getenv("PYTHONHOME"), "test.txt")
)
```
To read all SMS

```python
from kvdroid.tools.sms import get_all_sms
from android.permissions import Permission, request_permissions  # NOQA
# remember to add READ_SMS to your buildozer `android.permissions`

request_permissions([Permission.READ_SMS])
print(get_all_sms()) # returns a tuple of message count and messages
```

Since the release of Android 11 (API 30), the way file are stored became different
### License
MIT

