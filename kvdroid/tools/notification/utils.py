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
    NotificationBigTextStyle,
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


def _create_intent(
    extras, java_class, action, channel_id, notification_id, request_code
):
    if action != KVDROID_TAP_ACTION_NOTIFICATION:
        intent = IntentJava(activity, java_class)
        intent.setAction(action)
        intent.setPackage(activity.getPackageName())
        if extras:
            intent.putExtra(extras[0], String(extras[1]))
        intent.putExtra(EXTRA_NOTIFICATION_ID, notification_id)
        intent.putExtra(EXTRA_CHANNEL_ID, String(channel_id))
        return PendingIntentJava().getBroadcast(
            activity,
            request_code,
            intent,
            (
                PendingIntentJava().FLAG_MUTABLE
                | PendingIntentJava().FLAG_UPDATE_CURRENT
                if VERSION().SDK_INT >= 31
                else PendingIntentJava().FLAG_UPDATE_CURRENT
                | Notification().FLAG_AUTO_CANCEL
            ),
        )
    intent = IntentJava(activity, java_class)
    if extras:
        intent.putExtra(extras[0], String(extras[1]))
    intent.putExtra(EXTRA_NOTIFICATION_ID, notification_id)
    intent.putExtra(EXTRA_CHANNEL_ID, String(channel_id))
    intent.setFlags(
        IntentJava().FLAG_ACTIVITY_CLEAR_TOP | IntentJava().FLAG_ACTIVITY_SINGLE_TOP
    )
    intent.setAction(action)
    intent.addCategory(IntentJava().CATEGORY_LAUNCHER)
    return PendingIntentJava().getActivity(
        activity,
        request_code,
        intent,
        (
            PendingIntentJava().FLAG_IMMUTABLE
            if VERSION().SDK_INT >= 31
            else PendingIntentJava().FLAG_UPDATE_CURRENT
            | Notification().FLAG_AUTO_CANCEL
        ),
    )


def _build_notification_content(
    auto_cancel,
    channel_id,
    pending_intent,
    small_icon,
    small_icon_color,
    text,
    title,
    priority,
    defaults,
    builder,
    fullscreen,
    color,
    group_key,
    is_group_summary,
    number,
    ongoing,
    progress,
    input_history,
    vibrate_pattern,
    visibility,
    sound,
):
    builder.setSmallIcon(small_icon)
    if small_icon_color:
        try:
            builder.setColor(ContextCompat().getColor(activity, small_icon_color))
        except JavaException:
            builder.setColor(small_icon_color)
    builder.setContentTitle(String(title))
    builder.setContentText(String(text))
    # Set the intent that will fire when the user taps the notification
    builder.setContentIntent(pending_intent)
    builder.setWhen(System().currentTimeMillis())
    builder.setShowWhen(True)
    builder.setChannelId(channel_id)
    builder.setPriority(priority)
    builder.setDefaults(defaults)
    builder.setAutoCancel(auto_cancel)
    builder.setOngoing(ongoing)
    builder.setStyle(
        NotificationBigTextStyle(instantiate=True)
        .bigText(String(text))
        .setBigContentTitle(title)
    )
    if fullscreen:
        builder.setFullScreenIntent(pending_intent, True)
    if color is not None:
        builder.setColor(color)
        builder.setColorized(True)
    if group_key is not None:
        builder.setGroup(group_key)
        builder.setGroupSummary(is_group_summary)
    if number is not None:
        builder.setNumber(number)
    if progress is not None:
        builder.setProgress(*progress)
    if input_history is not None:
        builder.setRemoteInputHistory(input_history)
    if vibrate_pattern is not None:
        builder.setVibrate(vibrate_pattern)
    if visibility is not None:
        builder.setVisibility(visibility)
    if sound is not None:
        sound = Uri().parse(f"android.resource://{activity.getPackageName()}/{sound}")
        builder.setSound(sound)


def _build_notification_actions(
    action_title1,
    action_title2,
    action_title3,
    auto_cancel,
    key_text_reply,
    builder,
    extras,
    java_class,
    reply_title,
    channel_id,
    notification_id,
    request_code,
):
    if extra := action_title1 and extras.get("action1"):
        builder.addAction(
            get_resource_identifier("icon", "mipmap"),
            cast_object("charSequence", String(action_title1)),
            _create_intent(
                extra,
                java_class,
                KVDROID_ACTION_1_NOTIFICATION,
                channel_id,
                notification_id,
                request_code,
            ),
        )

    if extra := action_title2 and extras.get("action2"):
        builder.addAction(
            get_resource_identifier("icon", "mipmap"),
            cast_object("charSequence", String(action_title2)),
            _create_intent(
                extra,
                java_class,
                KVDROID_ACTION_2_NOTIFICATION,
                channel_id,
                notification_id,
                request_code,
            ),
        )

    if extra := action_title3 and extras.get("action3"):
        builder.addAction(
            get_resource_identifier("icon", "mipmap"),
            cast_object("charSequence", String(action_title3)),
            _create_intent(
                extra,
                java_class,
                KVDROID_ACTION_3_NOTIFICATION,
                channel_id,
                notification_id,
                request_code,
            ),
        )

    if extra := reply_title and extras.get("reply"):
        builder.addAction(
            NotificationCompatActionBuilder(
                get_resource_identifier("icon", "mipmap"),
                String(reply_title),
                _create_intent(
                    extra,
                    java_class,
                    KVDROID_REPLY_ACTION_NOTIFICATION,
                    channel_id,
                    notification_id,
                    request_code,
                ),
            )
            .addRemoteInput(
                RemoteInputBuilder(String(key_text_reply))
                .setLabel(String(reply_title))
                .build()
            )
            .build()
        ).setAutoCancel(auto_cancel)


def _set_big_picture(big_picture, builder):
    large_picture = NotificationCompatBigPictureStyle(instantiate=True)
    bitmap = get_bitmap(big_picture)
    large_picture.bigPicture(bitmap)
    builder.setStyle(large_picture)


def _set_large_icon(large_icon, builder):
    bitmap = get_bitmap(large_icon)
    builder.setLargeIcon(bitmap)
