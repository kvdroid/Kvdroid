# Kvdroid
Some Android tools for Kivy developments
### Dependencies
```sh
Android min-api21
```
### Requirements
```
kivy, android, jnius
 ```
### Installation

```
pip install kvdroid
```
### Usage
To detect keyboard height
```python
from kvdroid import keyboard_height
print(keyboard_height())
```
To detect if app is installed from Play Store or not
```python
from kvdroid.appsource import app_source
print(app_source)
```
To get absolute screen size in dp-pixel and detect current orientation
```python
from kvdroid.metrics import screen
print(screen.orientation())
print(screen.width_dp())
print(screen.height_px())
print(screen.resolution())
```
To check if device has a data connection both for wifi and cellular
```python
from kvdroid.network import network_state
print(network_state)
```
To check if device is  in dark mode or not
```python
from kvdroid.darkmode import dark_mode
print(dark_mode)
```
To get device informations.
Available options are;
```'model','brand','manufacturer','version','sdk','product','base','rom','security','hardware','tags','sdk_int','total_mem','used_mem','avail_ram','total_ram','used_ram','bat_level','bat_capacity','bat_tempeture','bat_voltage','bat_technology'```
```python
from kvdroid import device_info
print(device_info("model"))
print(device_info("avail_ram",convert = True))
```
To enable immersive mode
```python
from kvdroid import immersive_mode
immersive_mode(True) # default is False
```
To launch a specific app
```python
from kvdroid import launch_app  
launch_app(<app_package>,<app_activity>)
```
To open target app's details page
```python
from kvdroid import app_details
app_details(<app_package>)
```
To detect current device's language
```python
from kvdroid.lang import device_lang
print(device_lang)
```
To set statusbar color
```python
from kvdroid import statusbar_color
statusbar_color("#FFFFFF","black")
```
To set navigationbar color
```python
from kvdroid import navbar_color
navbar_color("#FFFFFF")
```
To display a toast message
```python
from kvdroid import toast
toast("hello world")
```
To get absolute sdcard path
```python
from kvdroid.path import sdcard
print(sdcard)
```
To get absolute external_sdcard
```python
from kvdroid.path import external_sdcard
print(external_sdcard)
```
To get path of working app folder
```python
from kvdroid.path import app_folder
print(app_folder)

```
To get file mime Type
```python
from kvdroid import mime_type
mime_type = mime_type(file_path)
print(mime_type)
```

To change default wallpaper
```python
from kvdroid import set_wallpaper
set_wallpaper("/sdcard/test.jpg")
```
To use text-to-speech
```python
from kvdroid import speech
speech("hello world", "en")
```
To use default Download Manager
```python
from kvdroid import download_manager
download_manager(<title>,<description>,<URL>,<path>,<file>)
```
To restart the app
```python
from kvdroid import restart_app
restart_app(True) # default is false
```
To share text via Android Share menu
```python
from kvdroid import share_text
share_text("hello world", title="Share", chooser=False, app_package=None, 
           call_playstore=False, error_msg="application unavailable")
```
To share any file via Android Share menu
```python
from kvdroid import share_file
share_file(<path-to-file>, <title>, <chooser>, <app-package: open-with-default-app>, 
    <call_playstore>, <error_msg>)
share_file("/sdcard/test.pdf", title='Share', chooser=False, app_package=None, 
           call_playstore=False, error_msg="application unavailable")
```
To play suported music format or radio stream through Android Media Player
```player.mPLayer = Android Media PLayer```
```python
from kvdroid.audio import player
player.play(<path-to-music-file>)
player.stream(Url) # radio
player.pause()
player.resume()
player.seek(value)
player.do_loop(True) # default is False
player.is_playing()
player.get_duration()
player.current_position()
```
To cast Java Object
```python
from kvdroid.cast import cast_object
from kvdroid import Uri
uri = Uri.fromFile("/home/java/my_document.pdf")
parcelable = cast_object("parcelable", uri)

# Above code  is same as below code::

from kvdroid.cast import cast_object
from kvdroid import Uri
from jnius import cast
uri = Uri.fromFile("/home/java/my_document.pdf")
parcelable = cast("android.os.Parcelabel", uri)

'''
 the difference is, you dont have to remember the package name, just only the name and 
 you are good to go. This will also be helpful for python devs who do have zero knowledge on java
 
 Note:: 
 not all castable java object are included you can open an issue to include all missing 
 castables
'''
```
### License
MIT

