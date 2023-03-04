from jnius import autoclass
from kvdroid.jclass import _class_call


def File(*args, instantiate: bool = False):
    return _class_call(autoclass('java.io.File'), args, instantiate)


def FileOutputStream(*args, instantiate: bool = False):
    return _class_call(autoclass('java.io.FileOutputStream'), args, instantiate)


def FileInputStream(*args, instantiate: bool = False):
    return _class_call(autoclass('java.io.FileInputStream'), args, instantiate)


def ByteArrayOutputStream(*args, instantiate: bool = False):
    return _class_call(autoclass('java.io.ByteArrayOutputStream'), args, instantiate)


def InputStream(*args, instantiate: bool = False):
    return _class_call(autoclass('java.io.InputStream'), args, instantiate)


def DataInputStream(*args, instantiate: bool = False):
    return _class_call(autoclass('java.io.DataInputStream'), args, instantiate)


def OutputStream(*args, instantiate: bool = False):
    return _class_call(autoclass('java.io.OutputStream'), args, instantiate)

