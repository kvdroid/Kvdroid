import logging
from os import environ

from jnius import autoclass


def _get_platform():
    # On Android sys.platform returns 'linux2', so prefer to check the
    # existence of environ variables set during Python initialization
    kivy_build = environ.get('KIVY_BUILD', '')
    if kivy_build in {'android', 'ios'}:
        return kivy_build
    elif 'P4A_BOOTSTRAP' in environ:
        return 'android'
    elif 'ANDROID_ARGUMENT' in environ:
        # We used to use this method to detect android platform,
        # leaving it here to be backwards compatible with `pydroid3`
        # and similar tools outside kivy's ecosystem
        return 'android'


platform = _get_platform()
Logger = logging.getLogger('kivy')

if platform == "android":
    try:
        from android import config

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
