from jnius import autoclass
from kvdroid.jclass import _class_call


def PickVisualMedia(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.activity.result.contract.ActivityResultContracts$PickVisualMedia"),
        args,
        instantiate
    )


def PickMultipleVisualMedia(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.activity.result.contract.ActivityResultContracts$PickMultipleVisualMedia"),
        args,
        instantiate
    )
