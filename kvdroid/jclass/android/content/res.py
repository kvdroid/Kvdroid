from jnius import autoclass
from kvdroid.jclass import _class_call


def Configuration(*args, instantiate: bool = False):
    return _class_call(autoclass("android.content.res.Configuration"), args, instantiate)
