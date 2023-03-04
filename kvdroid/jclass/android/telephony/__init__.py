from jnius import autoclass
from kvdroid.jclass import _class_call

def TelephonyManager(*args, instantiate: bool = False):
    return _class_call(autoclass("android.telephony.TelephonyManager"), args, instantiate)
