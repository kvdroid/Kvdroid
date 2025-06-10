from jnius import autoclass
from kvdroid.jclass import _class_call


def View(*args, instantiate: bool = False):
    return _class_call(autoclass('android.view.View'), args, instantiate)


def WindowManager(*args, instantiate: bool = False):
    return _class_call(autoclass("android.view.WindowManager"), args, instantiate)


def WindowManagerLayoutParams(*args, instantiate: bool = False):
    return _class_call(autoclass("android.view.WindowManager$LayoutParams"), args, instantiate)


def ViewGroupLayoutParams(*args, instantiate: bool = False):
    return _class_call(autoclass('android.view.ViewGroup$LayoutParams'), args, instantiate)


def TextureView(*args, instantiate: bool = False):
    return _class_call(autoclass('android.view.TextureView'), args, instantiate)


def WindowInsetsController(*args, instantiate: bool = False):
    return _class_call(autoclass('android.view.WindowInsetsController'), args, instantiate)


def Gravity(*args, instantiate: bool = False):
    return _class_call(autoclass('android.view.Gravity'), args, instantiate)
