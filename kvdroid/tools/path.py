import os
from jnius import cast
from kvdroid.jclass.android import Context, VERSION
from kvdroid.jclass.android.os import Environment
from kvdroid import activity


def sdcard(directory: str = "", slash: bool = False):
    dirs = {
        "alarm": Environment().DIRECTORY_ALARMS,
        "dcim": Environment().DIRECTORY_DCIM,
        "download": Environment().DIRECTORY_DOWNLOADS,
        "documents": Environment().DIRECTORY_DOCUMENTS,
        "movies": Environment().DIRECTORY_MOVIES,
        "music": Environment().DIRECTORY_MUSIC,
        "notifications": Environment().DIRECTORY_NOTIFICATIONS,
        "pictures": Environment().DIRECTORY_PICTURES,
        "podcasts": Environment().DIRECTORY_PODCASTS,
        "ringtones": Environment().DIRECTORY_RINGTONES
    }
    if not directory:
        return Environment().getExternalStorageDirectory().getAbsolutePath()
    else:
        if directory in dirs.keys():
            return Environment().getExternalStoragePublicDirectory(dirs[directory]).toString() + ("/" if slash else "")
        else:
            return None


def external_sdcard(slash: bool = False):
    try:
        return os.path.join("/storage", os.listdir("/storage")[1]) + ("/" if slash else "")
    except Exception:
        return None


def get_storage_volumes():
    path = []
    context = activity.getApplicationContext()
    storage_manager = cast(
        "android.os.storage.StorageManager",
        context.getSystemService(Context().STORAGE_SERVICE),
    )

    if storage_manager is not None:
        if VERSION().SDK_INT() >= 24:
            storage_volumes = storage_manager.getStorageVolumes()
            for storage_volume in storage_volumes:
                if storage_volume.isRemovable():
                    try:
                        directory = storage_volume.getDirectory()
                    except AttributeError:
                        directory = storage_volume.getPathFile()
                    path.append(directory.getAbsolutePath())
        else:
            storage_volumes = storage_manager.getVolumeList()
            for storage_volume in storage_volumes:
                if storage_volume.isRemovable():
                    path.append(storage_volume.getPath())

    return path if len(path) > 1 else path[0]
