from jnius import autoclass
from kvdroid.jclass import _class_call


def ViewCompat(*args, instantiate: bool = False):
    return _class_call(autoclass("androidx.core.view.ViewCompat"), args, instantiate)


def WindowCompat(*args, instantiate: bool = False):
    return _class_call(autoclass("androidx.core.view.WindowCompat"), args, instantiate)


def WindowInsetsCompat(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.core.view.WindowInsetsCompat"), args, instantiate
    )


def WindowInsetsCompatType(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.core.view.WindowInsetsCompat$Type"), args, instantiate
    )


def ViewGroupCompat(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.core.view.ViewGroupCompat"), args, instantiate
    )
