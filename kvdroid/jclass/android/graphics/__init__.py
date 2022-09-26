from jnius import autoclass
from kvdroid.jclass import _class_call


def Canvas(*args, instantiate: bool = False):
    return _class_call(autoclass("android.graphics.Canvas"), args, instantiate)


def Color(*args, instantiate: bool = False):
    return _class_call(autoclass("android.graphics.Color"), args, instantiate)


def Rect(*args, instantiate: bool = False):
    return _class_call(autoclass('android.graphics.Rect'), args, instantiate)


def Bitmap(*args, instantiate: bool = False):
    return _class_call(autoclass('android.graphics.Bitmap'), args, instantiate)


def BitmapFactory(*args, instantiate: bool = False):
    return _class_call(autoclass('android.graphics.BitmapFactory'), args, instantiate)


def Config(*args, instantiate: bool = False):
    return _class_call(autoclass("android.graphics.Bitmap$Config"), args, instantiate)


def CompressFormat(*args, instantiate: bool = False):
    return _class_call(autoclass("android.graphics.Bitmap$CompressFormat"), args, instantiate)


def Point(*args, instantiate: bool = False):
    return _class_call(autoclass("android.graphics.Point"), args, instantiate)
