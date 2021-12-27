from jnius import autoclass
from kvdroid.jclass import _class_call


def Toast(instantiate: bool=False, *args):
    return _class_call(autoclass('android.widget.Toast'), args, instantiate)
