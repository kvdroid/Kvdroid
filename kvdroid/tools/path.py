import os

from kvdroid.jclass.android.os import Environment


def path():
    return os.path.dirname(os.path.abspath("__main__"))


def sdcard():
    return Environment().getExternalStorageDirectory().toString()


def external_sdcard():
    try:
        return os.path.join("/storage", os.listdir("/storage")[1])
    except:
        return None
