KvDroid
=========

A re-implementation of android java API in python with easy access to some Android functionality like Notification,
Reading of Contacts, accessing Webview Cookies, etc...

The aim is to provide full access to Android API which can be used together with Python frameworks like:
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

```python
from kvdroid.jclass.android.graphics import Color
from kvdroid.tools.notification import (
    create_notification, 
    get_notification_reply_text,
    KVDROID_TAP_ACTION_NOTIFICATION,
    KVDROID_ACTION_1_NOTIFICATION,
    KVDROID_REPLY_ACTION_NOTIFICATION
)
from kvdroid.tools import get_resource
from kvdroid.tools.broadcast import BroadcastReceiver
from android.activuty import bind as activity_bind  # noqa


def perform_intent_action(intent):
    if extras := intent.getExtras():
        if value := extras.getString("tap"):
            # replace below code with whatever action you want to perform
            print("it is a tap")
            # incase you want to use the value too
            print(value)
        elif value := extras.getString("action1"):
            # replace below code with whatever action you want to perform
            print("it is an action1")
            # incase you want to use the value too
            print(value)
        elif value := extras.getString("reply"):
            # replace "TEST_KEY" with whatever 'key_reply_text' you used in creating
            # your notification
            reply = get_notification_reply_text(intent, "TEST_KEY")
            print(reply)
            # incase you want to use the value too
            print(value)


def get_notification_intent(intent):
    perform_intent_action(intent)


def get_notification_broadcast(context, intent):
    perform_intent_action(intent)
    
# This should be binded only once, else you get weird behaviors
# if you are creating different notifications for different purpose,
# you can bind different functions but only bind them once
activity_bind(on_new_intent=get_notification_intent)

br = BroadcastReceiver(
    callback=get_notification_broadcast, 
    actions=[
        KVDROID_TAP_ACTION_NOTIFICATION,
        KVDROID_ACTION_1_NOTIFICATION,
        KVDROID_REPLY_ACTION_NOTIFICATION
    ],
    use_intent_action=False
)
# start BroadcastReceiver before launching your notification.
br.start()

"""
stop your broad cast receiver when your app is closed
>>>
def on_stop(self):
    br.stop()
>>>
"""

create_notification(
    small_icon=get_resource("mipmap").icon,  # replace `.icon` with the image filename you set as your app icon without the file extension (e.g without .png, .jpg ...)
    channel_id="ch1", # you must set this to any string value of your choice
    title="You have a message", # title of your notification
    text="hi, just wanted to check on you", # notification content text
    ids=1, # notification id, can be used to update certain notification
    channel_name=f"message", # provides a user-friendly label for the channel, helping users understand the purpose or category of notifications associated with that channel.
    large_icon="assets/image.png",
    small_icon_color=Color().rgb(0x00, 0xC8, 0x53),  # 0x00 0xC8 0x53 is same as 00C853
    big_picture="assets/image.png",
    action_title1="action1",
    reply_title="reply",
    key_text_reply="TEST_KEY",
    # for effective use of this, please read the extras section of the documentation below
    # There are only 3 actions and 1 reply, but the 3 actions cannot exist together all at once
    # together with the reply. 1 of the actions must go.
    # The 3 actions must be declared with this names: 'action1', 'action2', 'action3'
    # the reply must retain the name: 'reply'. Same with tap: 'tap'
    extras={
        "tap": ("tap", "I tapped the notification"), 
        "action1": ("action1", "I pressed action1 button"),
        "reply": ("reply", "use get_notification_reply_text(intent, key_text_reply) to get my text")
    },
    # if you set this to true, it means that you don't want your app to open
    # when you tap on the notification or tap on any of the action button or reply
    # so you don't need to bind an intent function, here you make use of BrodcastReceiver
    # check the above code
    broadcast=False
)
```

Further notification description
```
:Parameters:
    `small_icon`: int
        The icon that appears at the top left conner of the android notification.
        Icon can be accessed by calling `get_resource(resource, activity_type=activity)`
        from kvdroid.tools module
    `channel_id`: str
        In Android, a channel ID is used to categorize and manage notifications.
        It's a unique identifier associated with a notification channel, which is
        a way to group and configure notifications in a specific way. Notification
        channels were introduced in Android Oreo (API level 26) to give users more
        control over how they receive and interact with notifications.
    `title`: str
        The title is a short, descriptive text that provides context for the
        notification's content. It's often displayed prominently at the top of the notification.
    `text`: str
        Text provides additional information related to the notification's title and
        helps users understand the purpose or context of the notification.
    `ids`: int
        The ids is an identifier used to uniquely identify a notification.
        It allows you to manage and update notifications, especially when you have
        multiple notifications displayed or want to update an existing notification with a new one.
    `channel_name`: str
        The channel_name is a human-readable name or description associated with a notification
        channel. It provides a user-friendly label for the channel, helping users understand
        the purpose or category of notifications associated with that channel.
    `large_icon`: Union[int, str, InputStream()]
        The large_icon is an optional image or icon that can be displayed alongside the
        notification's content. It's typically a larger image than the smallIcon and
        is used to provide additional context or visual appeal to the notification.
    `big_picture`: Union[int, str, InputStream()]
        the big_picture is a style of notification that allows you to display a large
        image, often associated with the notification's content. This style is
        particularly useful for notifications that include rich visual content,
        such as image-based messages or news articles.
    `action_title1`: str
        text that are displayed on notification buttons, used to also create notification
        buttons too.
    `action_title2`: str
        text that are displayed on notification buttons, used to also create notification
        buttons too.
    `action_title3`: str
        text that are displayed on notification buttons, used to also create notification
        buttons too.
    `key_text_reply`: str
        When you want to enable users to reply to notifications by entering text,
        you can use Remote Input, which is a feature that allows you to capture text input
        from users in response to a notification. key_text_reply is a symbolic
        representation or a constant used in your code to identify and process the
        user's text input when responding to notifications.
    `reply_title`: str
        text that is displayed on notification reply buttons, used to also create notification
        reply buttons too.
    `auto_cancel`: bool
        In Android notifications, the auto_cancel behavior is typically implemented by
        setting the setAutoCancel(true) method on the notification builder. When you
        set autoCancel to true, it means that the notification will be automatically
        canceled (dismissed) when the user taps on it. This is a common behavior for
        notifications where tapping the notification is expected to take the user to a
        corresponding activity or open a specific screen within the app.
    `extras`: dict
        A dictionary of string (keys) and tuple (values). Must be in this format
        ```python
        {
            "tap": (key, value),
            "action1": (key, value),
            "action2": (key, value),
            "action3": (key, value),
            "action1": (key, value),
            "reply": (key, value)
        }

        or 

        {"action1": (key, value)} or {"reply": (key, value)} or
        {"action1": (key, value), "reply": (key, value)} ...
        ```
        Extras are used to add additional data or key-value pairs to a notification.
        This allows you to attach custom data to a notification so that you can retrieve
        and process it when the user interacts with the notification
    `small_icon_color`: int
        the small_icon_color is primarily used to set the background color for the
        small icon in the notification header. It influences the color of the small
        circle that appears behind the small icon in the notification.

        Example using Color class from kvdroid.jclass.android module:
        `Color().BLUE`, `Color().rgb(0x00, 0xC8, 0x53),  # 0x00 0xC8 0x53 is same as 00C853`
    `java_class`: object
        an activity or any suitable java class
    `priority`: int
        the priority is used to set the priority level of a notification. The priority
        level determines how the notification should be treated in terms of importance
        and visibility. It helps the Android system and user to understand
        the significance of the notification.

        Here are the values that cn be used `from kvdroid.jclass.androidx` module:

        `NotificationCompat().PRIORITY_DEFAULT`:
            This is the default priority level. Notifications
            with this priority are treated as regular notifications. They are displayed in the
            notification shade but do not make any special sound or vibration. The user may see
            these notifications if they expand the notification shade.

        `NotificationCompat().PRIORITY_LOW`:
            Notifications with this priority are considered
            low-priority. They are displayed in a less prominent way and do not typically make a
            sound or vibration. They are often used for less important notifications that the user
            may not need to see immediately.

        `NotificationCompat().PRIORITY_MIN`:
            This is the minimum priority level. Notifications with
            this priority are considered the least important. They are not shown to the user unless the
            user explicitly opens the notification shade.

        `NotificationCompat().PRIORITY_HIGH:
            Notifications with this priority are considered high-priority.
            They are displayed prominently, may make a sound or vibration, and are intended to grab the user's
            attention. These are often used for important notifications that require immediate user interaction.

        `NotificationCompat().PRIORITY_MAX`:
            This is the maximum priority level. Notifications with this priority are treated as the most
            important and are displayed prominently with sound and vibration. They are typically used for
            critical notifications that require immediate attention.
    `defaults`: int
        the setDefaults() method is used to set the default behavior for a notification, such as whether
        it should make a sound, vibrate, or use the device's LED indicator. This method allows you to
        specify a combination of default notification behaviors.

        Here are the values that cn be used `from kvdroid.jclass.androidx` module:

        `NotificationCompat().DEFAULT_SOUND`: Use the default notification sound.
        `NotificationCompat().DEFAULT_VIBRATE: Make the device vibrate.
        `NotificationCompat().DEFAULT_LIGHTS`: Use the device's LED indicator (if available).
        `NotificationCompat().DEFAULT_ALL`: Use all default behaviors (sound, vibration, and LED).
    `broadcast`: bool
        sends out a broadcast message to your app to perform an action when an action button is
        clicked or reply is sent from your apps notification
:return: notification_manager
```
### To read Contacts

```python
from kvdroid.tools.contact import get_contact_details
#add this in buildozer permission 'android.permission.READ_CONTACTS'


def request_android_permissions(self):
    #call this function on_start function
    from android.permissions import request_permissions, Permission
    def callback(permissions, results):
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

### To get a specific app details

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
 
### To get an activity info

```python
from kvdroid.tools.package import activity_info

print(activity_info("com.android.settings","com.android.settings.network.NetworkSettings"))

"""
{'loadIcon': <android.graphics.drawable.Drawable at 0x7e8e15c46db0 jclass=android/graphics/drawable/Drawable jself=<LocalRef obj=0x6156 at 0x7e8e15c8c8b0>>,
 'loadLabel': 'Network and Internet'}
"""
```
 
### To save a drawable object to given path as png

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
### To detect if app is installed from Play Store or not

```python
from kvdroid.tools.appsource import app_source

print(app_source())
```

### To get application infos
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
print(app_dirs("ext_files"), slash = True) #/storage/sdcard0/Android/data/package/files/
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
### To check if device has a data connection.

```python
from kvdroid.tools.network import network_status, wifi_status, mobile_status, get_wifi_signal

print(network_status())  # for both wifi and mobile
print(wifi_status())    # only for wifi
print(mobile_status())    # only for mobile
print(get_wifi_signal())    # only for wifi
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

### To check if device is  in dark mode or not

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
### To open target app's details page

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

### To set statusbar color

```python
from kvdroid.tools import change_statusbar_color

change_statusbar_color("#FFFFFF", "black")
```
### To set navigationbar color

```python
from kvdroid.tools import navbar_color

navbar_color("#FFFFFF")
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
### To share any file via Android Share menu

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


### To access WebView cookies
(i.e if you compiled your app with webview bootstrap or have Webview in your app)

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
from kvdroid.tools import get_resource

drawable = get_resource("drawable")
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

Since the release of Android 11 (API 30), the way file are stored became different
### License
MIT

