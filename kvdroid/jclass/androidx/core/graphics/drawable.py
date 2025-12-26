from jnius import autoclass

from kvdroid.jclass import _class_call


def IconCompat(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.core.graphics.drawable.IconCompat"), args, instantiate
    )
