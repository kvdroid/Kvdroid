from jnius import autoclass
from kvdroid.jclass import _class_call


def Formatter(*args, instantiate: bool = False):
    return _class_call(autoclass('android.text.format.Formatter'), args, instantiate)
