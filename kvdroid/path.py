import os
from kvdroid import Environment


def path():
    return os.path.dirname(os.path.abspath("__main__"))


app_folder = path()


def sdcard():
    return Environment.getExternalStorageDirectory().toString()


sdcard = sdcard()


def external_sdcard():
    return os.path.join("/storage", os.listdir("/storage")[1])


external_sdcard = external_sdcard()
