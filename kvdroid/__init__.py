import logging
from os import environ
from typing import Union

from jnius import autoclass # NOQA


def _get_platform():
    # On Android sys.platform returns 'linux2', so prefer to check the
    # existence of environ variables set during Python initialization
    kivy_build = environ.get('KIVY_BUILD', '')
    if kivy_build in {'android', 'ios'}:
        return kivy_build
    elif 'P4A_BOOTSTRAP' in environ or 'ANDROID_ARGUMENT' in environ:
        return 'android'


def get_hex_from_color(color: list):
    return "#" + "".join([f"{int(i * 255):02x}" for i in color])


def _convert_color(color: Union[str, list]):
    if isinstance(color, list):
        color = get_hex_from_color(color)
    return color


platform = _get_platform()
Logger = logging.getLogger('kivy')

if platform != "android":
    raise ImportError("Kvdroid: Kvdroid is only callable from Android")
from android.config import ACTIVITY_CLASS_NAME, SERVICE_CLASS_NAME # NOQA

if 'PYTHON_SERVICE_ARGUMENT' in environ:
    PythonService = autoclass(SERVICE_CLASS_NAME)
    activity = PythonService.mService
else:
    PythonActivity = autoclass(ACTIVITY_CLASS_NAME)
    activity = PythonActivity.mActivity

packages = {
    "whatsapp": "com.whatsapp",
    "facebook": "com.facebook.katana",
    "facebookLite": "com.facebook.lite",
    "oldFacebook": "com.facebook.android",
    "linkedin": "com.linkedin.android",
    "fbMessenger": "com.facebook.orca",
    "fbMessengerLite": "com.facebook.mlite",
    "tiktok": "com.zhiliaoapp.musically",
    "tiktokLite": "com.zhiliaoapp.musically.go",
    "twitter": "com.twitter.android",
    "twitterLite": "com.twitter.android.lite",
    "telegram": "org.telegram.messenger",
    "telegramX": "org.thunderdog.challegram",
    "snapchat": "com.snapchat.android",
    "chrome": "com.android.chrome"
}
