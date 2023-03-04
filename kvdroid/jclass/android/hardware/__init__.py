from jnius import autoclass
from kvdroid.jclass import _class_call


def Camera(*args, instantiate: bool = False):
    return _class_call(autoclass("android.hardware.Camera"), args, instantiate)


def Sensor(*args, instantiate: bool = False):
    return _class_call(autoclass("android.hardware.Sensor"), args, instantiate)


def SensorManager(*args, instantiate: bool = False):
    return _class_call(autoclass("android.hardware.SensorManager"), args, instantiate)