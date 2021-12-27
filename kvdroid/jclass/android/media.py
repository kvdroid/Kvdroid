from jnius import autoclass
from kvdroid.jclass import _class_call


def MediaPlayer(instantiate: bool=False, *args):
    return _class_call(autoclass('android.media.MediaPlayer'), args, instantiate)


def AudioManager(instantiate: bool=False, *args):
    return _class_call(autoclass('android.media.AudioManager'), args, instantiate)
