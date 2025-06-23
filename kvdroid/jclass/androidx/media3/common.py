from jnius import autoclass
from kvdroid.jclass import _class_call


def MediaItem(*args, instantiate: bool = False):
    return _class_call(autoclass("androidx.media3.common.MediaItem"), args, instantiate)
