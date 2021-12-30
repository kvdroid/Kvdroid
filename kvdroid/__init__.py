import logging
from os import environ
from typing import Union

from jnius import autoclass


def _get_platform():
    # On Android sys.platform returns 'linux2', so prefer to check the
    # existence of environ variables set during Python initialization
    kivy_build = environ.get('KIVY_BUILD', '')
    if kivy_build in {'android', 'ios'}:
        return kivy_build
    elif 'P4A_BOOTSTRAP' in environ or 'ANDROID_ARGUMENT' in environ:
        return 'android'


def get_hex_from_color(color: list):
    return "#" + "".join([f"{i * 255:02x}" for i in color])


def _convert_color(color: Union[str, list]):
    if isinstance(color, list):
        color = get_hex_from_color(color)
    return color


platform = _get_platform()
Logger = logging.getLogger('kivy')

if platform == "android":
    try:
        from android import config # NOQA

        ns = config.JAVA_NAMESPACE
    except (ImportError, AttributeError):
        ns = 'org.renpy.android'

    if 'PYTHON_SERVICE_ARGUMENT' in environ:
        PythonService = autoclass(ns + '.PythonService')
        activity = PythonService.mService
    else:
        PythonActivity = autoclass(ns + '.PythonActivity')
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
        "snapchat": "com.snapchat.android"
    }
else:
    Logger.error(
        "Kvdroid: Kvdroid is only callable for Android"
    )
