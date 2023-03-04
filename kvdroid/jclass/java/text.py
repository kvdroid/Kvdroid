from jnius import autoclass
from kvdroid.jclass import _class_call


def SimpleDateFormat(*args, instantiate: bool = False):
    return _class_call(autoclass('java.text.SimpleDateFormat'), args, instantiate)


