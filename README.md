from kvdroid.tools.notification.constants import PendingIntentFlagKvDroid
=========

<!-- GitAds-Verify: FQNUQIK3LDGRA8V91UOY1X8PFDSEBSNR -->
## GitAds Sponsored
[![Sponsored by GitAds](https://gitads.dev/v1/ad-serve?source=kvdroid/kvdroid@github)](https://gitads.dev/v1/ad-track?source=kvdroid/kvdroid@github)



A re-implementation of android java API in python with easy access to some Android functionality like Notification,
Reading of Contacts, accessing Webview Cookies, etc...

The aim is to provide full access to Android API, which can be used together with Python frameworks like:
[kivy](https://github.com/kivy/kivy), [kivymd](https://github.com/kivymd/kivymd), etc... Or as a standalone, in which
Android native UI is created with only python codes.

## Compiling into APK
To compile, kivy [p4a](https://github.com/kivy/python-for-android) or kivy [buildozer](https://github.com/kivy/buildozer) is
required, and bootstrap must be set to `sdl2`
## Dependencies
```sh
Android min-api21
```

## Installation

```
pip install kvdroid

or

pip install https://github.com/kvdroid/Kvdroid/archive/refs/heads/master.zip # master version
# Note: this works on android only, but you can install it on your desktop for code completion assistance
```

## Buildozer Requirement
```
requirement = kvdroid

or

requirement = https://github.com/kvdroid/Kvdroid/archive/refs/heads/master.zip
```

## Usage


### To send notification

**Step 1: Create a notification channel (required for Android 8.0+)**

```python
from kvdroid.tools.notification.channel import NotificationChannel, create_notification_channel
from kvdroid.tools.notification.constants import Importance

# Create and configure a notification channel using the builder pattern
channel = (
    NotificationChannel(channel_id="messages", channel_name="Messages", importance=Importance.HIGH)
    .set_description("Notifications for new messages")
    .enable_vibration(True)
    .set_vibration_pattern([0, 300, 200, 300])
    .enable_lights(True)
    .set_show_badge(True)
)

# Register the channel with the system
create_notification_channel(channel)
```

**Step 2: Create and send notifications using the new builder API**

```python
from kvdroid.tools.notification.basic import Notification, create_notification
from kvdroid.tools import get_resource_identifier

# Build a simple notification using method chaining
notification = (
    Notification(channel_id="messages")
    .set_small_icon(get_resource_identifier("icon", "mipmap"))
    .set_content_title("New Message")
    .set_content_text("You have a new message!")
    .set_auto_cancel(True)
)

# Post the notification
manager = create_notification(1, notification)

# To cancel a notification later:
# manager.cancel(1)
```

**Advanced: Notification with actions and intents**

```python
from kvdroid.tools.notification.basic import Notification, create_notification
from kvdroid.tools.notification.utils import Intent, PendingIntent
from kvdroid.tools.notification.constants import PendingIntentFlag, Priority
from kvdroid.tools import get_resource_identifier
from kvdroid import get_android_sdk_int
from android import python_act  # noqa

# Create intents for tap and action buttons
tap_intent = (
    Intent()
    .set_action("TAP_ACTION")
    .put_extra("message_id", 12345)
)

flag = PendingIntentFlag.FLAG_IMMUTABLE if get_android_sdk_int() >= 31 else PendingIntentFlag.FLAG_UPDATE_CURRENT
tap_pending_intent = PendingIntent.get_activity(0, tap_intent, flag)

mark_read_intent = (
    Intent()
    .set_action("MARK_READ")
    .put_extra("action", "mark_read")
)

flag = (PendingIntentFlag.FLAG_MUTABLE | PendingIntentFlag.FLAG_UPDATE_CURRENT
        if get_android_sdk_int() >= 31 else PendingIntentFlag.FLAG_UPDATE_CURRENT)
mark_read_pending_intent = PendingIntent.get_broadcast(1, tap_intent, flag)

# Build notification with actions
notification = (
    Notification(channel_id="messages")
    .set_small_icon(get_resource_identifier("icon", "mipmap"))
    .set_content_title("New Message")
    .set_content_text("John: How are you?")
    .set_large_icon("assets/profile.png")
    .set_content_intent(tap_pending_intent)
    .add_action(0, "Mark Read", mark_read_pending_intent)
    .set_auto_cancel(True)
    .set_priority(Priority.HIGH)
)

# Post the notification
manager = create_notification(1, notification)
```

**Available notification builder methods:**

The `Notification` class supports extensive customization through these methods:
- **Content:** `set_content_title()`, `set_content_text()`, `set_sub_text()`, `set_ticker()`
- **Icons:** `set_small_icon()`, `set_large_icon()`, `set_color()`, `set_colorized()`
- **Actions:** `add_action()`, `set_content_intent()`, `set_delete_intent()`, `set_full_screen_intent()`
- **Behavior:** `set_auto_cancel()`, `set_ongoing()`, `set_silent()`, `set_only_alert_once()`
- **Priority:** `set_priority()`, `set_defaults()`
- **Grouping:** `set_group()`, `set_group_summary()`
- **Progress:** `set_progress(max, current, indeterminate)`
- **Badge:** `set_number()`, `set_show_badge()`
- **Alerts:** `set_sound()`, `set_vibrate()`, `set_lights()`, `enable_vibration()`
- **Visibility:** `set_visibility()`, `set_lockscreen_visibility()`
- **Timing:** `set_when()`, `set_timeout_after()`, `set_uses_chronometer()`
- **Styles:** `set_style()` (for big picture, big text, inbox, messaging styles)
- **Advanced:** `set_foreground_service_behavior()`, `set_remote_input_history()`, `set_shortcut_id()`

**To handle notification intents and actions:**

```python
from kvdroid.tools.broadcast import BroadcastReceiver
from android.activity import bind as activity_bind  # noqa

def handle_notification_action(intent):
    if extras := intent.getExtras():
        if message_id := extras.getString("message_id"):
            print(f"Notification tapped: {message_id}")
        elif action := extras.getString("action"):
            print(f"Action pressed: {action}")

def on_new_intent(intent):
    handle_notification_action(intent)

def on_broadcast(_, intent):
    handle_notification_action(intent)

# Bind activity intent handler (do this once)
activity_bind(on_new_intent=on_new_intent)

# Set up broadcast receiver for notification actions
br = BroadcastReceiver(
    callback=on_broadcast,
    actions=["TAP_ACTION", "ACTION_1"],
    use_intent_action=False
)
br.start()

# Stop broadcast receiver when app closes
# def on_stop(self):
#     br.stop()
```
### To read Contacts

```python
from kvdroid.tools.contact import get_contact_details
from android.permissions import request_permissions, Permission  # noqa

#add this in buildozer permission 'android.permission.READ_CONTACTS'


def callback(_, results):
    if all([res for res in results]):
        print("callback. All permissions granted.")
    else:
        print("callback. Some permissions refused.")

request_permissions([Permission.READ_CONTACTS, Permission.WRITE_CONTACTS, ], callback)


get_contact_details("phone_book") # gets a dictionary of all contact both contact name and phone mumbers
get_contact_details("names") # gets a list of all contact names
get_contact_details("mobile_no") # gets a list of all contact phone numbers
```

### To get a list of all installed packages (Applications)

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

### To get all main activities

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

### To check if the package is a system application

```python
from kvdroid.tools.package import is_system_package

print(is_system_package("com.android.settings"))
```

### To check if the package is enabled

```python
from kvdroid.tools.package import is_package_enabled

print(is_package_enabled("com.android.settings"))
```

### To get a specific app detail

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
 
### To get activity info

```python
from kvdroid.tools.package import activity_info

print(activity_info("com.android.settings","com.android.settings.network.NetworkSettings"))

"""
{'loadIcon': <android.graphics.drawable.Drawable at 0x7e8e15c46db0 jclass=android/graphics/drawable/Drawable jself=<LocalRef obj=0x6156 at 0x7e8e15c8c8b0>>,
 'loadLabel': 'Network and Internet'}
"""
```
 
### To save a drawable object to a given path as png

```python
from kvdroid.tools.package import package_info
from kvdroid.tools.graphics import save_drawable

app = package_info("com.android.settings")
app_icon = app["loadIcon"]

# <android.graphics.drawable.Drawable at 0x7e8e15c46db0 jclass=android/graphics/drawable/Drawable jself=<LocalRef obj=0x6156 at 0x7e8e15c8c8b0>>

save_drawable(app_icon, "< path >", "< file_name >")

# That will save the app icon to a given path and return the path + filename
# can be used like

from kivy.uix.image import Image

Image(source=save_drawable(app_icon, "< path >", "< file_name >"))
```


### To check if the given app is installed from PlayStore

```python
from kvdroid.tools.package import package_source

print(package_source("< package_name >"))
```

### To get Android WebView Cookies

```python
from kvdroid.tools.webkit import get_cookies

get_cookies("https://google.login")
```
### To detect keyboard height

```python
from kvdroid.tools import keyboard_height

print(keyboard_height())
```
### To detect if an app is installed from Play Store or not

```python
from kvdroid.tools.appsource import app_source

print(app_source())
```

### To get application info
`name` `pkg_name` `version_name` `version_code`

```python
from kvdroid.tools.appsource import app_info

print(app_info("name"))
```

### To get application directories
`data` `app` `files` `cache` `ext_files` `ext_cache`

```python
from kvdroid.tools.appsource import app_dirs

print(app_dirs("files")) #/data/data/package/files
```

### To get absolute screen size in dp-pixel and detect current orientation

```python
from kvdroid.tools.metrics import Metrics
screen = Metrics()

print(screen.orientation())
print(screen.width_dp())
print(screen.height_px())
print(screen.resolution())
```
### To check if a device has a data connection.

```python
from kvdroid.tools.network import network_status, wifi_status, mobile_status, get_wifi_signal

print(network_status())  # for both Wi-Fi and mobile
print(wifi_status())    # only for Wi-Fi
print(mobile_status())    # only for mobile
print(get_wifi_signal())    # only for Wi-Fi
```
### To get Wi-Fi signal strenght.

```python
from kvdroid.tools.network import  get_wifi_signal

print(get_wifi_signal()) 
```

### To get network latency.

```python
from kvdroid.tools.network import  network_latency

print(network_latency()) 
```

### To check if a device is in dark mode or not

```python
from kvdroid.tools.darkmode import dark_mode

print(dark_mode())
```
To get device informations.
Available options are;
```'model','brand','manufacturer','version','sdk','product','base','rom','security','hardware','tags','sdk_int','total_mem','used_mem','avail_ram','total_ram','used_ram','bat_level','bat_capacity','bat_temperature','bat_voltage','bat_technology', 'bat_status', 'bat_health'```

```python
from kvdroid.tools.deviceinfo import device_info

print(device_info("model"))
print(device_info("avail_ram", convert=True))
```
### To enable immersive mode

```python
from kvdroid.tools import immersive_mode

immersive_mode()
```
### To launch an application

```python
from kvdroid.tools import launch_app

launch_app("< app_package >")
```
### To launch a specific application activity

```python
from kvdroid.tools import launch_app_activity

launch_app_activity("< app_package >", "< app_activity >")
```
### To open the target app's details page

```python
from kvdroid.tools import app_details

app_details("< app_package >")
```
### To detect current device's language

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

### To get a list of supported languages on the device

```python
from kvdroid.tools.lang import supported_languages
print(supported_languages())

"""
['af', 'agq', 'ak', 'am', 'ar', 'as', 'asa', 'ast'...]
"""
```

### To set the statusbar color

```python
from kvdroid.tools import change_statusbar_color

# This won't work on API 35 (android 15) and above.
# Android advices to enable edge-to-edge instead.
# To enable edge-to-edge, use this function `enable_edge_to_edge()`.
change_statusbar_color(background_color="#FFFFFF", foreground_color="black")
```
### To set navigationbar color

```python
from kvdroid.tools import navbar_color

navbar_color(background_color="#FFFFFF", foreground_color="white")
```
### To display a toast message

```python
from kvdroid.tools import toast

toast("hello world")
```
### To get absolute sdcard path and media directories
`alarm` `dcim` `download` `documents` `movies` `music` `notifications` `pictures` `podcasts` `ringtones`

```python
from kvdroid.tools.path import sdcard

print(sdcard()) #/storage/sdcard0
print(sdcard("download")) #/storage/sdcard0/Download
print(sdcard("download", slash = True)) #/storage/sdcard0/Download/

```
### To get absolute external_sdcard

```python
from kvdroid.tools.path import external_sdcard

print(external_sdcard()) 
```
### To get file mime Type

```python
from kvdroid.tools import mime_type

mime_type = mime_type("path/to/file")
print(mime_type)
```

### To change default wallpaper

```python
from kvdroid.tools import set_wallpaper

set_wallpaper("/sdcard/test.jpg")
```
### To use text-to-speech

```python
from kvdroid.tools import speech

speech("hello world", "en")
```
### To use default Download Manager

```python
from kvdroid.tools import download_manager

download_manager("< title >", "< description >", "< URL >", "< path >", "< file >")
```
### To restart the app

```python
from kvdroid.tools import restart_app

restart_app()
```
### To share text via Android Share menu

```python
from kvdroid.tools import share_text

share_text("hello world", title="Share", chooser=False, app_package=None,
           call_playstore=False, error_msg="application unavailable")
```
### To share any file via the Android Share menu

```python
from kvdroid.tools import share_file

share_file(
    "< path - to - file >", "< title >", "< chooser >", "< app - package: open -with-default - app >",
    "< call_playstore >", "< error_msg >")
share_file("/sdcard/test.pdf", title='Share', chooser=False, app_package=None,
           call_playstore=False, error_msg="application unavailable")
```
### To play supported music format or radio stream through Android Media Player
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

### To use system-provided fonts

:warning: `That function is so experimental. It should work for Android 7 and above but not been tested on much devices. It is actually for multilingual purposes to use system-provided fonts for no Latin languages. system_font() will always return the supported font from /system/fonts for the current device language.  Also, you could use any language-supported font from the system just by calling the system_font function with the target language's iso639-1 or iso639-2 abbreviation such as font_name = system_font('zh') or system_font('zho'). `

```python
from kivy.uix.label import Label
from kvdroid.tools.font import system_font

# that will return the default font for the device's current language.
Label(text = "example", font_name = system_font())

# for the specific language font
Label(text = "你好世界", font_name = system_font('zho')) # Language definition must be iso639-1 or iso639-2 abbreviation.  https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
```

### To cast Java Object

```python
from kvdroid.cast import cast_object
from kvdroid.jclass.android import Uri

uri = Uri().fromFile("/home/java/my_document.pdf")
parcelable = cast_object("parcelable", uri)

# The above code is same as the below code::

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


### To access WebView cookies
(i.e., if you compiled your app with webview bootstrap or have Webview in your app)

```python
from kvdroid.tools.webkit import get_cookies

print(get_cookies("https://google.com"))
```
### To access android package resource folders like:
- drawable
- layout
- menu
- values
- mipmap
- etc....

```python
from kvdroid.tools import get_resource_identifier

icon = get_resource_identifier("icon", "mipmap")
```
### To get Wi-Fi IP Address
```python
from kvdroid.tools.network import get_wifi_ip_address
print(get_wifi_ip_address())
```
### To send email
```python
from kvdroid.tools.email import send_email
send_email(
    recipient=["test@gmail.com"], 
    subject="Hello there", 
    body="This is kvdroid"
)
```
### To send an email with an attachment (androidx is required)
Also note before you can share files on an Android version greater \
than 10, you must specify a provider in the AndroidManifest.xml \
inside the \<application> tag e.g.
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
and also specify a file path in the res/xml/filepath.xml of the android project folder e.g.
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
### To read all SMS

```python
from kvdroid.tools.sms import get_all_sms
from android.permissions import Permission, request_permissions  # NOQA
# remember to add READ_SMS to your buildozer `android.permissions`

request_permissions([Permission.READ_SMS])
print(get_all_sms()) # returns a tuple of message count and messages
```
### To read all Call Log

```python
from kvdroid.tools.call import get_call_log
from android.permissions import Permission, request_permissions  # NOQA
# remember to add READ_CALL_LOG to your buildozer `android.permissions`

request_permissions([Permission.READ_CALL_LOG])
print(get_call_log()) # returns a tuple of call log count and call_log
```

### To enable edge-to-edge

```python
from kvdroid.tools.display import enable_edge_to_edge

enable_edge_to_edge()
```

### To set edge-to-edge manually

```python
from kvdroid.tools.display import set_edge_to_edge_manually

set_edge_to_edge_manually()
```

### To get navbar height and statusbar height
```python
from kvdroid.tools.display import get_navbar_height, get_statusbar_height

sh = get_statusbar_height()
nh = get_navbar_height()
```

### To set screen orientation
```python
from kvdroid.tools import set_orientation

# Set to portrait mode
set_orientation("portrait")

# Other available modes: 'landscape', 'sensor', 'user', 'behind', 'full_sensor',
# 'full_user', 'locked', 'no_sensor', 'user_portrait', 'user_landscape',
# 'unspecified', 'sensor_portrait', 'sensor_landscape', 'reverse_portrait', 'reverse_landscape'
```

### To check keyboard visibility and get its height
```python
from kvdroid.tools import check_keyboard_visibility_and_get_height

is_visible, height = check_keyboard_visibility_and_get_height()
print(f"Keyboard visible: {is_visible}, Height: {height}px")
```

### To use Android Photo Picker
```python
from kvdroid.tools.photo_picker import (
    pick_image_only,
    pick_video_only,
    pick_image_and_video,
    is_photo_picker_available,
    get_pick_images_max_limit
)

def callback(uris):
    if uris:
        for uri in uris:
            print(f"Selected: {uri}")

# Check if photo picker is available (Android 11+ with specific extensions or Android 13+)
if is_photo_picker_available():
    # Pick single image
    pick_image_only(multiple=False, callback=callback)

    # Pick multiple images (up to system limit)
    pick_image_only(multiple=True, callback=callback)

    # Pick video only
    pick_video_only(multiple=False, callback=callback)

    # Pick both images and videos
    pick_image_and_video(multiple=True, callback=callback)

    # Get maximum number of images that can be picked
    max_limit = get_pick_images_max_limit()
    print(f"Max images: {max_limit}")
```

### To resolve URI to file path
```python
from kvdroid.tools.uri import resolve_uri

# Resolve a content:// URI to an actual file path
file_path = resolve_uri(uri)
print(file_path)
```

### To grant or revoke URI permissions
```python
from kvdroid.tools.uri import grant_uri_permission, revoke_uri_permission
from kvdroid.jclass.android import Intent

# Grant URI permission to another app
intent = Intent()
permissions = Intent().FLAG_GRANT_READ_URI_PERMISSION
grant_uri_permission(intent, uri, permissions)

# Revoke URI permission
revoke_uri_permission(uri, permissions)
```

### To convert Android Bitmap to Kivy Texture
```python
from kvdroid.tools.kivytools import bitmap_to_texture
from kivy.uix.image import Image

# Convert Android bitmap to Kivy texture
texture = bitmap_to_texture(bitmap)

# Use in Kivy Image widget
img = Image()
img.texture = texture
```

### To use ExoPlayer for advanced media playback
```python
from kvdroid.tools.exoplayer import ExoPlayer

# Create ExoPlayer instance
player = ExoPlayer()

# Create media item from URI or file
media_item = ExoPlayer.media_item_from_uri("https://example.com/music.mp3")
# or from file
media_item = ExoPlayer.media_item_from_file("/sdcard/music.mp3")

# Set media item and prepare
player.set_media_item(media_item)
player.prepare()

# Playback controls
player.play()
player.pause()
player.seek_to(5000)  # Seek to 5 seconds

# Check player state
if player.is_playing():
    position = player.get_current_position()
    duration = player.get_duration()
    print(f"Position: {position}ms / {duration}ms")

# Set repeat mode
player.set_repeat_mode(ExoPlayer.REPEAT_MODE_ALL)

# Enable shuffle
player.set_shuffle_mode_enabled(True)

# Add multiple media items
media_items = [
    ExoPlayer.media_item_from_file("/sdcard/song1.mp3"),
    ExoPlayer.media_item_from_file("/sdcard/song2.mp3"),
]
player.set_media_items(media_items)

# Navigate between media items
player.seek_to_next_media_item()
player.seek_to_previous_media_item()

# Clear all media items
player.clear_media_items()
```

### To use BroadcastReceiver
```python
from kvdroid.tools.broadcast import BroadcastReceiver

def on_broadcast(context, intent):
    action = intent.getAction()
    print(f"Received broadcast: {action}")

# Create broadcast receiver with system actions
br = BroadcastReceiver(
    callback=on_broadcast,
    actions=["BATTERY_LOW", "SCREEN_ON"],  # Will be expanded to ACTION_BATTERY_LOW, etc.
    use_intent_action=True
)

# Or with custom actions
br = BroadcastReceiver(
    callback=on_broadcast,
    actions=["com.example.CUSTOM_ACTION"],
    use_intent_action=False
)

# Start listening
br.start()

# Stop listening when done
br.stop()
```

### To get system bar heights

```python
from kvdroid.jinterface.view import Insets
from kvdroid.tools.display import set_on_apply_window_insets_listener, request_apply_insets


def on_apply_window_insets(insets: Insets):
    print(insets.top, insets.bottom, insets.left, insets.right)
    

set_on_apply_window_insets_listener(on_apply_window_insets)
request_apply_insets()
```

### License
MIT

