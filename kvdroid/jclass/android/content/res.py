from jnius import autoclass
from kvdroid.jclass import _class_call


def Configuration(*args, instantiate: bool = False):
    return _class_call(autoclass("android.content.res.Configuration"), args, instantiate)


def Resources(*args, instantiate: bool = False):
    return _class_call(autoclass("android.content.res.Resources"), args, instantiate)

def TypedArray(*args, instantiate: bool = False):
    return _class_call(autoclass("android.content.res.TypedArray"), args, instantiate)
