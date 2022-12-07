import os

from kvdroid.jclass.android.os import Environment


def path():
    return os.path.dirname(os.path.abspath("__main__"))


def sdcard(directory: str = "",  slash: bool = False):
    dirs = {
        "alarm": Environment().DIRECTORY_ALARMS,
        "dcim":  Environment().DIRECTORY_DCIM,
        "download": Environment().DIRECTORY_DOWNLOADS,
        "documents": Environment().DIRECTORY_DOCUMENTS,
        "movies": Environment().DIRECTORY_MOVIES,
        "music": Environment().DIRECTORY_MUSIC,
        "notifications": Environment().DIRECTORY_NOTIFICATIONS,
        "pictures": Environment().DIRECTORY_PICTURES,
        "podcasts": Environment().DIRECTORY_PODCASTS,
        "ringtones": Environment().DIRECTORY_RINGTONES,
        }
    if not directory:
        return Environment().getExternalStorageDirectory().toString()
    else:
        if directory in dirs.keys():
            return Environment().getExternalStoragePublicDirectory(dirs[directory]).toString() + ( "/" if slash else "")
        else:
            return None


def external_sdcard():
    try:
        return os.path.join("/storage", os.listdir("/storage")[1])
    except Exception:
        return None
