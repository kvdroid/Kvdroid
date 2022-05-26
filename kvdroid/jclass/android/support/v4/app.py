from jnius import autoclass
from kvdroid.jclass import _class_call


def ActivityCompat(*args, instantiate: bool = False):
    return _class_call(autoclass("android.support.v4.app.ActivityCompat"), args, instantiate)
