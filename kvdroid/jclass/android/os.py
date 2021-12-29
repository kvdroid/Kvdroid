from jnius import autoclass
from kvdroid.jclass import _class_call


def Environment(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.Environment"), args, instantiate)


def Build(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.Build"), args, instantiate)


def VERSION(*args, instantiate: bool = False):
    return _class_call(autoclass('android.os.Build$VERSION'), args, instantiate)


def VERSION_CODES(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.Build$VERSION_CODES"), args, instantiate)


def StrictMode(*args, instantiate: bool = False):
    return _class_call(autoclass('android.os.StrictMode'), args, instantiate)


def StatFs(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.StatFs"), args, instantiate)


def BatteryManager(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.BatteryManager"), args, instantiate)
