from jnius import autoclass
from kvdroid.jclass import _class_call


def URLConnection(*args, instantiate: bool = False):
    return _class_call(autoclass("java.net.URLConnection"), args, instantiate)


def HttpURLConnection(*args, instantiate: bool = False):
    return _class_call(autoclass("java.net.HttpURLConnection"), args, instantiate)


def URL(*args, instantiate: bool = False):
    return _class_call(autoclass("java.net.URL"), args, instantiate)


def Socket(*args, instantiate: bool = False):
    return _class_call(autoclass("java.net.Socket"), args, instantiate)


def InetAddress(*args, instantiate: bool = False):
    return _class_call(autoclass("java.net.InetAddress"), args, instantiate)
