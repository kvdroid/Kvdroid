from jnius import autoclass, JavaException

from kvdroid.jclass import _browserx_except_cls_call


def CustomTabsIntent(*args, instantiate: bool = False):
    return _browserx_except_cls_call(
        "androidx.browser.customtabs.CustomTabsIntent", args, instantiate)


def CustomTabsIntentBuilder(*args, instantiate: bool = False):
    return _browserx_except_cls_call(
        "androidx.browser.customtabs.CustomTabsIntent$Builder", args, instantiate)


def CustomTabColorSchemeParams(*args, instantiate: bool = False):
    return _browserx_except_cls_call(
        "androidx.browser.customtabs.CustomTabColorSchemeParams", args, instantiate)


def CustomTabColorSchemeParamsBuilder(*args, instantiate: bool = False):
    return _browserx_except_cls_call(
        "androidx.browser.customtabs.CustomTabColorSchemeParams$Builder", args, instantiate)
