from jnius import autoclass
from kvdroid.jclass import _class_call


def PickVisualMediaRequestBuilder(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.activity.result.PickVisualMediaRequest$Builder"),
        args,
        instantiate
    )
