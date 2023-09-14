from jnius import autoclass
from kvdroid.jclass import _class_call
from android.config import ACTIVITY_CLASS_NAME, SERVICE_CLASS_NAME, JAVA_NAMESPACE  # NOQA


def PythonActivity(*args, instantiate: bool = False):
    return _class_call(autoclass(ACTIVITY_CLASS_NAME), args, instantiate)


def PythonService(*args, instantiate: bool = False):
    return _class_call(autoclass(SERVICE_CLASS_NAME), args, instantiate)


def GenericBroadcastReceiver(*args, instantiate: bool = False):
    return _class_call(autoclass(f"{JAVA_NAMESPACE}.GenericBroadcastReceiver"), args, instantiate)
