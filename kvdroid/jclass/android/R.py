from jnius import autoclass
from kvdroid.jclass import _class_call


def Dimen(*args, instantiate: bool = False):
    return _class_call(autoclass("android.R$dimen"), args, instantiate)
