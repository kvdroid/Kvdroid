from jnius import autoclass
from kvdroid.jclass import _class_call


def ExoPlayer(*args, instantiate: bool = False):
    return _class_call(autoclass("androidx.media3.exoplayer.ExoPlayer"), args, instantiate)


def ExoPlayerBuilder(*args, instantiate: bool = False):
    return _class_call(autoclass("androidx.media3.exoplayer.ExoPlayer$Builder"), args, instantiate)
