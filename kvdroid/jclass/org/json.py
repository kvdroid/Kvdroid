from jnius import autoclass
from kvdroid.jclass import _class_call


def JSONArray(*args, instantiate: bool = False):
    return _class_call(autoclass('org.json.JSONArray'), args, instantiate)


def JSONObject(*args, instantiate: bool = False):
    return _class_call(autoclass('org.json.JSONObject'), args, instantiate)
