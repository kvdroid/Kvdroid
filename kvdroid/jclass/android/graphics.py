from jnius import autoclass
from kvdroid.jclass import _class_call


def Color(*args, instantiate: bool = False):
    return _class_call(autoclass("android.graphics.Color"), args, instantiate)


def Rect(*args, instantiate: bool = False):
    return _class_call(autoclass('android.graphics.Rect'), args, instantiate)


def BitmapFactory(*args, instantiate: bool = False):
    return _class_call(autoclass('android.graphics.BitmapFactory'), args, instantiate)


def Point(*args, instantiate: bool = False):
    return _class_call(autoclass("android.graphics.Point"), args, instantiate)