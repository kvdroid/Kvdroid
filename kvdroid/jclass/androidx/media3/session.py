from jnius import autoclass

from kvdroid.jclass import _class_call


def MediaStyleNotificationHelperMediaStyle(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.media3.session.MediaStyleNotificationHelper$MediaStyle"),
        args,
        instantiate,
    )
