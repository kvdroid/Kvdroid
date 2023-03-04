from jnius import autoclass
from kvdroid.jclass import _class_call


def Toast(*args, instantiate: bool = False):
    return _class_call(autoclass('android.widget.Toast'), args, instantiate)


def RelativeLayout(*args, instantiate: bool = False):
    return _class_call(autoclass('android.widget.RelativeLayout'), args, instantiate)


def LinearLayout(*args, instantiate: bool = False):
    return _class_call(autoclass('android.widget.LinearLayout'), args, instantiate)


def TextView(*args, instantiate: bool = False):
    return _class_call(autoclass('android.widget.TextView'), args, instantiate)
