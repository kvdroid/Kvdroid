from jnius import autoclass
from kvdroid.jclass import _class_call


def Runtime(*args, instantiate: bool = False):
    return _class_call(autoclass('java.lang.Runtime'), args, instantiate)


def String(*args, instantiate: bool = False):
    return _class_call(autoclass("java.lang.String"), args, instantiate)


def StringBuffer(*args, instantiate: bool = False):
    return _class_call(autoclass("java.lang.StringBuffer"), args, instantiate)


def StringBuilder(*args, instantiate: bool = False):
    return _class_call(autoclass("java.lang.StringBuilder"), args, instantiate)


def System(*args, instantiate: bool = False):
    return _class_call(autoclass("java.lang.System"), args, instantiate)


def Long(*args, instantiate: bool = False):
    return _class_call(autoclass("java.lang.Long"), args, instantiate)


def Array(*args, instantiate: bool = False):
    return _class_call(autoclass("java.lang.reflect.Array"), args, instantiate)