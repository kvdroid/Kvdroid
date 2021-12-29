from jnius import autoclass
from kvdroid.jclass import _class_call


def File(*args, instantiate: bool = False):
    return _class_call(autoclass('java.io.File'), args, instantiate)
