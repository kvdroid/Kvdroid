from jnius import autoclass
from kvdroid.jclass import _class_call


def Locale(*args, instantiate: bool = False):
    return _class_call(autoclass('java.util.Locale'), args, instantiate)


def ArrayList(*args, instantiate: bool = False):
    return _class_call(autoclass('java.util.ArrayList'), args, instantiate)
