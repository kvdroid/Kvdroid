from jnius import autoclass

from kvdroid import require_api
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
    return _class_call(
        autoclass("android.content.pm.ApplicationInfo"), args, instantiate
    )


def Fragment(*args, instantiate: bool = False):
    return _class_call(autoclass("android.app.Fragment"), args, instantiate)


def FragmentManager(*args, instantiate: bool = False):
    return _class_call(autoclass("android.app.FragmentManager"), args, instantiate)


def NotificationManager(*args, instantiate: bool = False):
    return _class_call(autoclass("android.app.NotificationManager"), args, instantiate)


def Notification(*args, instantiate: bool = False):
    return _class_call(autoclass("android.app.Notification"), args, instantiate)


@require_api(">=", 26)
def NotificationChannel(*args, instantiate: bool = False):
    return _class_call(
        autoclass("android.app.NotificationChannel"), args, instantiate
    )


def WallpaperManager(*args, instantiate: bool = False):
    return _class_call(autoclass("android.app.WallpaperManager"), args, instantiate)


def Request(*args, instantiate: bool = False):
    return _class_call(
        autoclass("android.app.DownloadManager$Request"), args, instantiate
    )


def PendingIntent(*args, instantiate: bool = False):
    return _class_call(autoclass("android.app.PendingIntent"), args, instantiate)


def MemoryInfo(*args, instantiate: bool = False):
    return _class_call(
        autoclass("android.app.ActivityManager$MemoryInfo"), args, instantiate
    )


def PersonBuilder(*args, instantiate: bool = False):
    return _class_call(autoclass("android.app.Person$Builder"), args, instantiate)


@require_api(">=", 31)
def NotificationCallStyle(*args, instantiate: bool = False):
    return _class_call(
        autoclass("android.app.Notification$CallStyle"), args, instantiate
    )


@require_api(">=", 36)
def NotificationProgressStyle(*args, instantiate: bool = False):
    return _class_call(
        autoclass("android.app.Notification$ProgressStyle"), args, instantiate
    )


@require_api(">=", 36)
def NotificationProgressStylePoint(*args, instantiate: bool = False):
    return _class_call(
        autoclass("android.app.Notification$ProgressStyle$Point"), args, instantiate
    )


@require_api(">=", 36)
def NotificationProgressStyleSegment(*args, instantiate: bool = False):
    return _class_call(
        autoclass("android.app.Notification$ProgressStyle$Segment"), args, instantiate
    )
