from jnius import autoclass
from kvdroid.jclass import _class_call


def AppCompatActivity(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.appcompat.app.AppCompatActivity"),
        args,
        instantiate
    )
