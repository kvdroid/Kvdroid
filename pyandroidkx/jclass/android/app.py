from os import environ
from jnius import autoclass
from pyandroidkx.jclass.android.os import VERSION

NotificationManager = autoclass("android.app.NotificationManager")
Notification = autoclass("android.app.Notification")
if VERSION.SDK_INT >= 26:
    NotificationChannel = autoclass("android.app.NotificationChannel")
WallpaperManager = autoclass('android.app.WallpaperManager')
Request = autoclass("android.app.DownloadManager$Request")
AndroidActivity = autoclass('android.app.Activity')
PendingIntent = autoclass("android.app.PendingIntent")
MemoryInfo = autoclass('android.app.ActivityManager$MemoryInfo')