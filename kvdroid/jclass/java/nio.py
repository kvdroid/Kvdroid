from jnius import autoclass

from kvdroid.jclass import _class_call


def ByteBuffer(*args, instantiate: bool = False):
    return _class_call(autoclass("java.nio.ByteBuffer"), args, instantiate)