import os
from kvdroid import Environment


def path():
    return os.path.dirname(os.path.abspath("__main__"))


app_folder = path()


def sdcard():
    return Environment.getExternalStorageDirectory().toString()


sdcard = sdcard()
