from jnius import autoclass
from kvdroid.jclass import _class_call


def StreamConfigurationMap(*args, instantiate: bool = False):
    return _class_call(autoclass("android.hardware.camera2.params.StreamConfigurationMap"), args, instantiate)
