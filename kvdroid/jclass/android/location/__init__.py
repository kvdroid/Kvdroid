from jnius import autoclass
from kvdroid.jclass import _class_call


def LocationManager(*args, instantiate: bool = False):
    return _class_call(autoclass("android.location.LocationManager"), args, instantiate)

