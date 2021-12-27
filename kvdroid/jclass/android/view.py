from jnius import autoclass
from kvdroid.jclass import _class_call


def View(*args, instantiate: bool = False):
    return _class_call(autoclass('android.view.View'), args, instantiate)


def WindowManager(*args, instantiate: bool = False):
    return _class_call(autoclass("android.view.WindowManager"), args, instantiate)


def LayoutParams(*args, instantiate: bool = False):
    return _class_call(autoclass("android.view.WindowManager$LayoutParams"), args, instantiate)
