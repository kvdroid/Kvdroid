from jnius import autoclass
from kvdroid.jclass import _class_call

if autoclass("android.os.Build$VERSION").SDK_INT >= 26:

    def NotificationManagerCompat(*args, instantiate: bool = False):
        return _class_call(
            autoclass("androidx.core.app.NotificationManagerCompat"), args, instantiate
        )


def NotificationCompat(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.core.app.NotificationCompat"), args, instantiate
    )


def NotificationCompatBigPictureStyle(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.core.app.NotificationCompat$BigPictureStyle"),
        args,
        instantiate,
    )


def NotificationCompatAction(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.core.app.NotificationCompat$Action"), args, instantiate
    )


def NotificationCompatActionBuilder(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.core.app.NotificationCompat$Action$Builder"),
        args,
        instantiate,
    )


def NotificationCompatBuilder(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.core.app.NotificationCompat$Builder"), args, instantiate
    )


def NotificationBigTextStyle(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.core.app.NotificationCompat$BigTextStyle"),
        args,
        instantiate,
    )


def RemoteInput(*args, instantiate: bool = False):
    return _class_call(autoclass("androidx.core.app.RemoteInput"), args, instantiate)


def RemoteInputBuilder(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.core.app.RemoteInput$Builder"), args, instantiate
    )


def NotificationCompatMessagingStyle(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.core.app.NotificationCompat$MessagingStyle"),
        args,
        instantiate,
    )


def NotificationCompatMessagingStyleMessage(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.core.app.NotificationCompat$MessagingStyle$Message"),
        args,
        instantiate,
    )


def NotificationCompatInboxStyle(*args, instantiate: bool = False):
    return _class_call(
        autoclass("androidx.core.app.NotificationCompat$InboxStyle"), args, instantiate
    )
