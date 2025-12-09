from jnius import autoclass
from kvdroid.jclass import _class_call


def Intent(*args, instantiate: bool = False):
    return _class_call(autoclass("android.content.Intent"), args, instantiate)


def Context(*args, instantiate: bool = False):
    return _class_call(autoclass("android.content.Context"), args, instantiate)


def IntentFilter(*args, instantiate: bool = False):
    return _class_call(autoclass("android.content.IntentFilter"), args, instantiate)


def ContentValues(*args, instantiate: bool = False):
    return _class_call(autoclass("android.content.ContentValues"), args, instantiate)


def ContentUris(*args, instantiate: bool = False):
    return _class_call(autoclass("android.content.ContentUris"), args, instantiate)


def SharedPreferences(*args, instantiate: bool = False):
    return _class_call(
        autoclass("android.content.SharedPreferences"), args, instantiate
    )


def BroadcastReceiver(*args, instantiate: bool = False):
    return _class_call(
        autoclass("android.content.BroadcastReceiver"), args, instantiate
    )


def ContentResolver(*args, instantiate: bool = False):
    return _class_call(autoclass("android.content.ContentResolver"), args, instantiate)


def ComponentName(*args, instantiate: bool = False):
    return _class_call(autoclass("android.content.ComponentName"), args, instantiate)
