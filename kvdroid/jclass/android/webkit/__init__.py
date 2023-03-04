from jnius import autoclass
from kvdroid.jclass import _class_call


def CookieManager(*args, instantiate: bool = False):
    return _class_call(autoclass("android.webkit.CookieManager"), args, instantiate)


def URLUtil(*args, instantiate: bool = False):
    return _class_call(autoclass("android.webkit.URLUtil"), args, instantiate)


def MimeTypeMap(*args, instantiate: bool = False):
    return _class_call(autoclass('android.webkit.MimeTypeMap'), args, instantiate)


def WebView(*args, instantiate: bool = False):
    return _class_call(autoclass('android.webkit.WebView'), args, instantiate)