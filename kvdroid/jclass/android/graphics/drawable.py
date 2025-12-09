from jnius import autoclass
from kvdroid.jclass import _class_call


def BitmapDrawable(*args, instantiate: bool = False):
    return _class_call(
        autoclass("android.graphics.drawable.BitmapDrawable"), args, instantiate
    )


def Drawable(*args, instantiate: bool = False):
    return _class_call(
        autoclass("android.graphics.drawable.Drawable"), args, instantiate
    )


def AdaptiveIconDrawable(*args, instantiate: bool = False):
    return _class_call(
        autoclass("android.graphics.drawable.AdaptiveIconDrawable"), args, instantiate
    )


def Icon(*args, instantiate: bool = False):
    return _class_call(autoclass("android.graphics.drawable.Icon"), args, instantiate)
