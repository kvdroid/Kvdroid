from jnius import autoclass
from kvdroid.jclass import _class_call


def Runtime(*args, instantiate: bool = False):
    return _class_call(autoclass('java.lang.Runtime'), args, instantiate)


def String(*args, instantiate: bool = False):
    return _class_call(autoclass("java.lang.String"), args, instantiate)


def System(*args, instantiate: bool = False):
    return _class_call(autoclass("java.lang.System"), args, instantiate)
