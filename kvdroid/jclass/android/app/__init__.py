from jnius import autoclass
from kvdroid.jclass import _class_call


def Activity(*args, instantiate: bool = False):
    return _class_call(autoclass("android.app.Activity"), args, instantiate)


def ActivityManager(*args, instantiate: bool = False):
    return _class_call(autoclass("android.app.ActivityManager"), args, instantiate)


def AlarmManager(*args, instantiate: bool = False):
    return _class_call(autoclass("android.app.AlarmManager"), args, instantiate)


def AlertDialog(*args, instantiate: bool = False):
    return _class_call(autoclass("android.app.AlertDialog"), args, instantiate)


def Application(*args, instantiate: bool = False):
    return _class_call(autoclass("android.app.Application"), args, instantiate)


def ApplicationInfo(*args, instantiate: bool = False):
    return _class_call(autoclass("android.content.pm.ApplicationInfo"), args, instantiate)


def Fragment(*args, instantiate: bool = False):
    return _class_call(autoclass("android.app.Fragment"), args, instantiate)


def FragmentManager(*args, instantiate: bool = False):
    return _class_call(autoclass("android.app.FragmentManager"), args, instantiate)


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


def PendingIntent(*args, instantiate: bool = False):
    return _class_call(autoclass("android.app.PendingIntent"), args, instantiate)


def MemoryInfo(*args, instantiate: bool = False):
    return _class_call(autoclass('android.app.ActivityManager$MemoryInfo'), args, instantiate)

    
def ComponentName(*args, instantiate: bool = False):
    return _class_call(autoclass("android.content.ComponentName"), args, instantiate)


def ActivityInfo(*args, instantiate: bool = False):
    return _class_call(autoclass('android.content.pm.ActivityInfo'), args, instantiate)


def PackageManager(*args, instantiate: bool = False):
    return _class_call(autoclass("android.content.pm.PackageManager"), args, instantiate)

    
def Configuration(*args, instantiate: bool = False):
    return _class_call(autoclass("android.content.res.Configuration"), args, instantiate)
