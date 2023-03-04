from jnius import autoclass
from kvdroid.jclass import _class_call


def Uri(*args, instantiate: bool = False):
    return _class_call(autoclass('android.net.Uri'), args, instantiate)


def ConnectivityManager(*args, instantiate: bool = False):
    return _class_call(autoclass("android.net.ConnectivityManager"), args, instantiate)


def NetworkInfo(*args, instantiate: bool = False):
    return _class_call(autoclass("android.net.NetworkInfo"), args, instantiate)
