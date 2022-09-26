from jnius import autoclass
from kvdroid.jclass import _class_call


def Size(*args, instantiate: bool = False):
    return _class_call(autoclass("android.util.Size"), args, instantiate)
