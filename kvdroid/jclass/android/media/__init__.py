from jnius import autoclass
from kvdroid.jclass import _class_call


def ImageReader(*args, instantiate: bool = False):
    return _class_call(autoclass("android.media.ImageReader"), args, instantiate)


def MediaPlayer(instantiate: bool = False, *args):
    return _class_call(autoclass("android.media.MediaPlayer"), args, instantiate)


def AudioManager(instantiate: bool = False, *args):
    return _class_call(autoclass("android.media.AudioManager"), args, instantiate)


def AudioAttributes(instantiate: bool = False, *args):
    return _class_call(autoclass("android.media.AudioAttributes"), args, instantiate)


def AudioAttributesBuilder(instantiate: bool = False, *args):
    return _class_call(
        autoclass("android.media.AudioAttributes$Builder"), args, instantiate
    )
