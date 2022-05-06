from jnius import autoclass
from kvdroid.jclass import _class_call


def WifiManager(*args, instantiate: bool = False):
    return _class_call(autoclass('android.net.wifi.WifiManager'), args, instantiate)
