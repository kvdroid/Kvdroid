from jnius import autoclass
from kvdroid.jclass import _class_call


def NotificationManager(*args, instantiate: bool = False):
    return _class_call(autoclass("android.app.NotificationManager"), args, instantiate)


def Notification(*args, instantiate: bool = False):
    return _class_call(autoclass("android.app.Notification"), args, instantiate)


if autoclass('android.os.Build$VERSION').SDK_INT >= 26:
    def NotificationChannel(*args, instantiate: bool = False):
        return _class_call(autoclass("android.app.NotificationChannel"), args, instantiate)


def WallpaperManager(*args, instantiate: bool = False):
    return _class_call(autoclass('android.app.WallpaperManager'), args, instantiate)


def Request(*args, instantiate: bool = False):
    return _class_call(autoclass("android.app.DownloadManager$Request"), args, instantiate)


def Activity(*args, instantiate: bool = False):
    return _class_call(autoclass('android.app.Activity'), args, instantiate)


def PendingIntent(*args, instantiate: bool = False):
    return _class_call(autoclass("android.app.PendingIntent"), args, instantiate)


def MemoryInfo(*args, instantiate: bool = False):
    return _class_call(autoclass('android.app.ActivityManager$MemoryInfo'), args, instantiate)


def ActivityManager(*args, instantiate: bool = False):
    return _class_call(autoclass("android.app.ActivityManager"), args, instantiate)
