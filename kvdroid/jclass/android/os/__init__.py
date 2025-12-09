from jnius import autoclass
from kvdroid.jclass import _class_call


def AsyncTask(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.AsyncTask"), args, instantiate)


def Environment(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.Environment"), args, instantiate)


def BatteryManager(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.BatteryManager"), args, instantiate)


def Build(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.Build"), args, instantiate)


def Bundle(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.Bundle"), args, instantiate)


def Debug(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.Debug"), args, instantiate)


def FileUtils(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.FileUtils"), args, instantiate)


def Handler(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.Handler"), args, instantiate)


def HandlerThread(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.HandlerThread"), args, instantiate)


def Looper(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.Looper"), args, instantiate)


def Message(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.Message"), args, instantiate)


def Parcelable(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.Parcelable"), args, instantiate)


def PowerManager(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.PowerManager"), args, instantiate)


def Process(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.Process"), args, instantiate)


def Vibrator(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.Vibrator"), args, instantiate)


def VibrationEffect(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.VibrationEffect"), args, instantiate)


def VERSION(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.Build$VERSION"), args, instantiate)


def VERSION_CODES(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.Build$VERSION_CODES"), args, instantiate)


def StrictMode(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.StrictMode"), args, instantiate)


def StatFs(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.StatFs"), args, instantiate)


def SystemClock(*args, instantiate: bool = False):
    return _class_call(autoclass("android.os.SystemClock"), args, instantiate)
