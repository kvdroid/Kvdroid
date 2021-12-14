from jnius import JavaException, autoclass
from pyandroidkx import Logger
from pyandroidkx.jclass.android.os import VERSION

try:
    if VERSION.SDK_INT >= 26:
        NotificationManagerCompat = autoclass("androidx.core.app.NotificationManagerCompat")
    NotificationCompat = autoclass("androidx.core.app.NotificationCompat")
    NotificationCompatBigPictureStyle = autoclass("androidx.core.app.NotificationCompat$BigPictureStyle")
    NotificationCompatAction = autoclass("androidx.core.app.NotificationCompat$Action")
    NotificationCompatActionBuilder = autoclass("androidx.core.app.NotificationCompat$Action$Builder")
    NotificationCompatBuilder = autoclass("androidx.core.app.NotificationCompat$Builder")
    NotificationBigTextStyle = autoclass("androidx.core.app.NotificationCompat$BigTextStyle")
    RemoteInput = autoclass("androidx.core.app.RemoteInput")
    RemoteInputBuilder = autoclass("androidx.core.app.RemoteInput$Builder")
except JavaException:
    Logger.error("Kvdroid: Androidx Not Enabled. Skipping....")
