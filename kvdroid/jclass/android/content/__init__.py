from jnius import autoclass
from kvdroid.jclass import _class_call


def Intent(*args, instantiate: bool = False):
    return _class_call(autoclass("android.content.Intent"), args, instantiate)


def Context(*args, instantiate: bool = False):
    return _class_call(autoclass("android.content.Context"), args, instantiate)


def IntentFilter(*args, instantiate: bool = False):
    return _class_call(autoclass("android.content.IntentFilter"), args, instantiate)
