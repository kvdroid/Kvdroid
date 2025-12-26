__all__ = ("Intent", "PendingIntent")

from jnius import JavaException
from android import python_act  # NOQA
from kvdroid import activity
from kvdroid.cast import cast_object
from kvdroid.jclass.android import (
    Intent as IntentJava,
    PendingIntent as PendingIntentJava,
    VERSION,
    Notification,
    Uri,
)
from kvdroid.jclass.androidx import (
    ContextCompat,
    NotificationCompatBigTextStyle,
    NotificationCompatActionBuilder,
    RemoteInputBuilder,
    NotificationCompatBigPictureStyle,
)
from kvdroid.jclass.java import String, System
from kvdroid.tools import get_resource_identifier
from kvdroid.tools.graphics import get_bitmap
from kvdroid.tools.notification.constants import (
    KVDROID_REPLY_ACTION_NOTIFICATION,
    KVDROID_ACTION_1_NOTIFICATION,
    KVDROID_ACTION_2_NOTIFICATION,
    KVDROID_ACTION_3_NOTIFICATION,
    KVDROID_TAP_ACTION_NOTIFICATION,
    EXTRA_NOTIFICATION_ID,
    EXTRA_CHANNEL_ID,
    PendingIntentFlag,
)


class Intent:
    __slots__ = ("intent",)

    def __init__(self, java_class=None):
        self.intent = IntentJava(activity, java_class or python_act._class)

    def set_action(self, action: str):
        self.intent.setAction(action)
        return self

    def set_package(self, package_name: str):
        self.intent.setPackage(package_name)
        return self

    def put_extra(self, key: str, value):
        self.intent.putExtra(key, value)
        return self

    def get_intent(self):
        return self.intent


class PendingIntent:
    @staticmethod
    def get_broadcast(
        request_code: int, intent: Intent, flags: PendingIntentFlag, context=None
    ):
        return PendingIntentJava().getBroadcast(
            context or activity, request_code, intent.get_intent(), flags.value
        )

    @staticmethod
    def get_activity(
        request_code: int, intent: Intent, flags: PendingIntentFlag, context=None
    ):
        return PendingIntentJava().getActivity(
            context or activity, request_code, intent.get_intent(), flags.value
        )

    @staticmethod
    def get_foreground_service(
        request_code: int, intent: Intent, flags: PendingIntentFlag, context=None
    ):
        return PendingIntentJava().getForegroundService(
            context or activity, request_code, intent.get_intent(), flags.value
        )

    @staticmethod
    def get_service(
        request_code: int, intent: Intent, flags: PendingIntentFlag, context=None
    ):
        return PendingIntentJava().getService(
            context or activity, request_code, intent.get_intent(), flags.value
        )
