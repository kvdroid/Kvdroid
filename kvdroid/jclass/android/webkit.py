from jnius import autoclass
from kvdroid.jclass import _class_call


def CookieManager(*args, instantiate: bool = False):
    return _class_call(autoclass("android.webkit.CookieManager"), args, instantiate)
