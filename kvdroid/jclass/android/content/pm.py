from jnius import autoclass
from kvdroid.jclass import _class_call


def PackageManager(*args, instantiate: bool = False):
    return _class_call(
        autoclass("android.content.pm.PackageManager"), args, instantiate
    )


def ActivityInfo(*args, instantiate: bool = False):
    return _class_call(autoclass("android.content.pm.ActivityInfo"), args, instantiate)
