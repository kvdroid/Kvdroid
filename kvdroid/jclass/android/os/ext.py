from jnius import autoclass

from kvdroid.jclass import _class_call


def SdkExtensions(*args, instantiate: bool = False):
    return _class_call(autoclass('android.os.ext.SdkExtensions'), args, instantiate)
