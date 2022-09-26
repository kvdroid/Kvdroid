from jnius import autoclass
from kvdroid.jclass import _class_call


def CameraDevice(*args, instantiate: bool = False):
    return _class_call(autoclass("android.hardware.camera2.CameraDevice"), args, instantiate)


def CameraCaptureSession(*args, instantiate: bool = False):
    return _class_call(autoclass("android.hardware.camera2.CameraCaptureSession"), args, instantiate)


def CaptureRequest(*args, instantiate: bool = False):
    return _class_call(autoclass("android.hardware.camera2.CaptureRequest"), args, instantiate)


def CaptureRequestBuilder(*args, instantiate: bool = False):
    return _class_call(autoclass("android.hardware.camera2.CaptureRequest$Builder"), args, instantiate)


def CameraManager(*args, instantiate: bool = False):
    return _class_call(autoclass("android.hardware.camera2.CameraManager"), args, instantiate)


def CameraCharacteristics(*args, instantiate: bool = False):
    return _class_call(autoclass("android.hardware.camera2.CameraCharacteristics"), args, instantiate)
