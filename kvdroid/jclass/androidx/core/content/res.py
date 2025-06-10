from jnius import autoclass
from kvdroid.jclass import _class_call


def ResourcesCompat(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.core.content.res.ResourcesCompat"), args, instantiate)
