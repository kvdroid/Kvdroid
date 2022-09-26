from jnius import autoclass
from kvdroid.jclass import _class_call


def ContextCompat(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.core.content.ContextCompat"), args, instantiate)


def FileProvider(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.core.content.FileProvider"), args, instantiate)
