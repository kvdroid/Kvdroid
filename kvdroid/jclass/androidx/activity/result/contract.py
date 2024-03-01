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


def PickVisualMediaImageAndVideo(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.activity.result.contract.ActivityResultContracts$PickVisualMedia$ImageAndVideo"),
        args,
        instantiate
    )


def PickVisualMediaImageOnly(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.activity.result.contract.ActivityResultContracts$PickVisualMedia$ImageOnly"),
        args,
        instantiate
    )


def PickVisualMediaVideoOnly(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.activity.result.contract.ActivityResultContracts$PickVisualMedia$VideoOnly"),
        args,
        instantiate
    )


def PickVisualMediaSingleMimeType(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.activity.result.contract.ActivityResultContracts$PickVisualMedia$SingleMimeType"),
        args,
        instantiate
    )
