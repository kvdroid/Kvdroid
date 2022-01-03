import os

from kvdroid.jclass.android.os import Environment


def path():
    return os.path.dirname(os.path.abspath("__main__"))


app_folder = path()


def sdcard():
    return Environment().getExternalStorageDirectory().toString()


sdcard = sdcard()


def external_sdcard():
    try:
        return os.path.join("/storage", os.listdir("/storage")[1])
    except:
        return None


external_sdcard = external_sdcard()
