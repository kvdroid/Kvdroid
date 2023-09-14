"""
Androidx Notification
=====================
"""

from typing import Union
from jnius import cast, JavaException  # NOQA
from android import python_act  # NOQA
from kvdroid import Logger, activity
from kvdroid.cast import cast_object
from kvdroid.jclass.java import InputStream
from kvdroid.tools import get_resource

try:
    from kvdroid.jclass.androidx import (
        ContextCompat,
        NotificationCompatBuilder,
        NotificationCompat,
        NotificationCompatActionBuilder,
        RemoteInputBuilder,
        NotificationCompatBigPictureStyle,
        NotificationBigTextStyle,
        RemoteInput
    )
    from kvdroid.jclass.android import (
        Intent,
        Context,
        PendingIntent,
        NotificationManager,
        Notification,
        NotificationChannel,
        BitmapFactory,
        VERSION
    )
    from kvdroid.jclass.java.lang import String, System
    from kvdroid.jclass.org import GenericBroadcastReceiver
    from kvdroid.tools.broadcast import BroadcastReceiver

    KVDROID_REPLY_ACTION_NOTIFICATION = f'{activity.getPackageName()}.KVDROID_REPLY_ACTION_NOTIFICATION'
    KVDROID_ACTION_1_NOTIFICATION = f'{activity.getPackageName()}.KVDROID_ACTION_1_NOTIFICATION'
    KVDROID_ACTION_2_NOTIFICATION = f'{activity.getPackageName()}.KVDROID_ACTION_2_NOTIFICATION'
    KVDROID_ACTION_3_NOTIFICATION = f'{activity.getPackageName()}.KVDROID_ACTION_3_NOTIFICATION'
    KVDROID_TAP_ACTION_NOTIFICATION = f'{activity.getPackageName()}.KVDROID_TAP_ACTION_NOTIFICATION'


    def _create_intent(extras, java_class, broadcast, broadcast_action):
        if broadcast:
            intent = Intent(broadcast_action)
            if extras:
                intent.putExtra(*extras)
            return PendingIntent().getBrodcast(activity, 0, intent, PendingIntent().FLAG_UPDATE_CURRENT)
        intent = Intent(activity, java_class)
        if extras:
            intent.putExtra(*extras)
        intent.setFlags(Intent().FLAG_ACTIVITY_CLEAR_TOP | Intent().FLAG_ACTIVITY_SINGLE_TOP)
        intent.setAction(Intent().ACTION_MAIN)
        intent.addCategory(Intent().CATEGORY_LAUNCHER)
        return PendingIntent().getActivity(
            activity,
            0,
            intent,
            PendingIntent().FLAG_MUTABLE
            if VERSION().SDK_INT >= 31
            else PendingIntent().FLAG_UPDATE_CURRENT | Notification().FLAG_AUTO_CANCEL,
        )


    def _create_notification_channel(channel_id, channel_name, notification_manager):
        importance = NotificationManager().IMPORTANCE_HIGH
        channel = NotificationChannel(String(channel_id), String(channel_name), importance)
        channel.setDescription("notification")
        # Register the channel with the system; you can't change the importance
        # or other notification behaviors after this
        notification_manager.createNotificationChannel(channel)


    def _build_notification_content(auto_cancel, channel_id, pending_intent, small_icon, small_icon_color, text,
                                    title, priority, defaults, builder):
        builder.setSmallIcon(small_icon)
        if small_icon_color:
            try:
                builder.setColor(ContextCompat().getColor(activity.getApplicationContext(), small_icon_color))
            except JavaException:
                builder.setColor(small_icon_color)
        builder.setContentTitle(String(title))
        builder.setContentText(String(text))
        # Set the intent that will fire when the user taps the notification
        builder.setContentIntent(pending_intent)
        builder.setWhen(System().currentTimeMillis())
        builder.setChannelId(String(channel_id))
        builder.setPriority(priority)
        builder.setDefaults(defaults)
        builder.setAutoCancel(auto_cancel)
        builder.setTicker(String(""))
        builder.setContentInfo("INFO")
        builder.setStyle(NotificationBigTextStyle(instantiate=True).bigText(String(text)).setBigContentTitle(title))


    def _build_notification_actions(action_title1, action_title2, action_title3, auto_cancel, key_text_reply,
                                    builder, extras, java_class, reply_title, broadcast):
        if extra := action_title1 and extras.get("action1"):
            builder.addAction(
                get_resource("mipmap").icon,
                cast_object("charSequence", String(action_title1)),
                _create_intent(extra, java_class, broadcast, KVDROID_ACTION_1_NOTIFICATION)
            )

        if extra := action_title2 and extras.get("action2"):
            builder.addAction(
                get_resource("mipmap").icon,
                cast_object("charSequence", String(action_title2)),
                _create_intent(extra, java_class, broadcast, KVDROID_ACTION_2_NOTIFICATION)
            )

        if extra := action_title3 and extras.get("action3"):
            builder.addAction(
                get_resource("mipmap").icon,
                cast_object("charSequence", String(action_title3)),
                _create_intent(extra, java_class, broadcast, KVDROID_ACTION_3_NOTIFICATION)
            )

        if extra := reply_title and extras.get("reply"):
            builder.addAction(
                NotificationCompatActionBuilder(
                    get_resource("mipmap").icon,
                    String(reply_title),
                    _create_intent(extra, java_class, broadcast, KVDROID_REPLY_ACTION_NOTIFICATION)
                ).addRemoteInput(
                    RemoteInputBuilder(String(key_text_reply)).setLabel(String(reply_title)).build()
                ).build()
            ).setAutoCancel(auto_cancel)


    def _set_big_picture(big_picture, builder):
        large_picture = NotificationCompatBigPictureStyle(instantiate=True)
        if isinstance(big_picture, int):
            large_picture.bigPicture(BitmapFactory().decodeResource(activity.getResources(), big_picture))
        elif isinstance(big_picture, str):
            large_picture.bigPicture(BitmapFactory().decodeFile(big_picture))
        else:
            large_picture.bigPicture(BitmapFactory().decodeStream(big_picture))
        builder.setStyle(large_picture)


    def _set_large_icon(large_icon, builder):
        if isinstance(large_icon, int):
            builder.setLargeIcon(BitmapFactory().decodeResource(activity.getResources(), large_icon))
        elif isinstance(large_icon, str):
            builder.setLargeIcon(BitmapFactory().decodeFile(large_icon))
        else:
            builder.setLargeIcon(BitmapFactory().decodeStream(large_icon))


    def create_notification(
            small_icon: int,
            channel_id: str,
            title: str,
            text: str,
            ids: int,
            channel_name: str,
            large_icon: Union[int, str, InputStream()] = None,
            big_picture: Union[int, str, InputStream()] = None,
            action_title1: str = None,
            action_title2: str = None,
            action_title3: str = None,
            key_text_reply: str = None,
            reply_title: str = None,
            auto_cancel: bool = True,
            extras: dict = None,
            small_icon_color: int = None,
            java_class: object = None,
            priority: int = None,
            defaults: int = None,
            broadcast=False
    ) -> object:  # sourcery no-metrics
        """
        A convenience function that encapsulates the process of creating a
        notification using the NotificationCompat.Builder class or the Notification.Builder class.
        This function helps simplify the code and make it more readable.

        :Parameters:
            `small_icon`: int
                The icon that appears at the top left conner of the android notification.
                Icon can be accessed by calling `get_resource(resource, activity_type=activity)`
                from kvdroid.tools module
            `channel_id`: str
                In Android, a channel ID is used to categorize and manage notifications.
                It's a unique identifier associated with a notification channel, which is
                a way to group and configure notifications in a specific way. Notification
                channels were introduced in Android Oreo (API level 26) to give users more
                control over how they receive and interact with notifications.
            `title`: str
                The title is a short, descriptive text that provides context for the
                notification's content. It's often displayed prominently at the top of the notification.
            `text`: str
                Text provides additional information related to the notification's title and
                helps users understand the purpose or context of the notification.
            `ids`: int
                The ids is an identifier used to uniquely identify a notification.
                It allows you to manage and update notifications, especially when you have
                multiple notifications displayed or want to update an existing notification with a new one.
            `channel_name`: str
                The channel_name is a human-readable name or description associated with a notification
                channel. It provides a user-friendly label for the channel, helping users understand
                the purpose or category of notifications associated with that channel.
            `large_icon`: Union[int, str, InputStream()]
                The large_icon is an optional image or icon that can be displayed alongside the
                notification's content. It's typically a larger image than the smallIcon and
                is used to provide additional context or visual appeal to the notification.
            `big_picture`: Union[int, str, InputStream()]
                the big_picture is a style of notification that allows you to display a large
                image, often associated with the notification's content. This style is
                particularly useful for notifications that include rich visual content,
                such as image-based messages or news articles.
            `action_title1`: str
                text that are displayed on notification buttons, used to also create notification
                buttons too.
            `action_title2`: str
                text that are displayed on notification buttons, used to also create notification
                buttons too.
            `action_title3`: str
                text that are displayed on notification buttons, used to also create notification
                buttons too.
            `key_text_reply`: str
                When you want to enable users to reply to notifications by entering text,
                you can use Remote Input, which is a feature that allows you to capture text input
                from users in response to a notification. key_text_reply is a symbolic
                representation or a constant used in your code to identify and process the
                user's text input when responding to notifications.
            `reply_title`: str
                text that is displayed on notification reply buttons, used to also create notification
                reply buttons too.
            `auto_cancel`: bool
                In Android notifications, the auto_cancel behavior is typically implemented by
                setting the setAutoCancel(true) method on the notification builder. When you
                set autoCancel to true, it means that the notification will be automatically
                canceled (dismissed) when the user taps on it. This is a common behavior for
                notifications where tapping the notification is expected to take the user to a
                corresponding activity or open a specific screen within the app.
            `extras`: dict
                A dictionary of string (keys) and tuple (values). Must be in this format
                ```
                {
                    "tap": (key, value),
                    "action1": (key, value),
                    "action2": (key, value),
                    "action3": (key, value),
                    "action1": (key, value),
                    "reply": (key, value)
                }

                or {"action1": (key, value)} or {"reply": (key, value)} or
                {"action1": (key, value), "reply": (key, value)} ...
                ```
                Extras are used to add additional data or key-value pairs to a notification.
                This allows you to attach custom data to a notification so that you can retrieve
                and process it when the user interacts with the notification
            `small_icon_color`: int
                the small_icon_color is primarily used to set the background color for the
                small icon in the notification header. It influences the color of the small
                circle that appears behind the small icon in the notification.

                Example using Color class from kvdroid.jclass.android module:
                `Color().BLUE`, `Color().rgb(0x00, 0xC8, 0x53),  # 0x00 0xC8 0x53 is same as 00C853`
            `java_class`: object
                an activity or any suitable java class
            `priority`: int
                the priority is used to set the priority level of a notification. The priority
                level determines how the notification should be treated in terms of importance
                and visibility. It helps the Android system and user to understand
                the significance of the notification.

                Here are the values that cn be used `from kvdroid.jclass.androidx` module:

                `NotificationCompat().PRIORITY_DEFAULT`:
                    This is the default priority level. Notifications
                    with this priority are treated as regular notifications. They are displayed in the
                    notification shade but do not make any special sound or vibration. The user may see
                    these notifications if they expand the notification shade.

                `NotificationCompat().PRIORITY_LOW`:
                    Notifications with this priority are considered
                    low-priority. They are displayed in a less prominent way and do not typically make a
                    sound or vibration. They are often used for less important notifications that the user
                    may not need to see immediately.

                `NotificationCompat().PRIORITY_MIN`:
                    This is the minimum priority level. Notifications with
                    this priority are considered the least important. They are not shown to the user unless the
                    user explicitly opens the notification shade.

                `NotificationCompat().PRIORITY_HIGH:
                    Notifications with this priority are considered high-priority.
                    They are displayed prominently, may make a sound or vibration, and are intended to grab the user's
                    attention. These are often used for important notifications that require immediate user interaction.

                `NotificationCompat().PRIORITY_MAX`:
                    This is the maximum priority level. Notifications with this priority are treated as the most
                    important and are displayed prominently with sound and vibration. They are typically used for
                    critical notifications that require immediate attention.
            `defaults`: int
                the setDefaults() method is used to set the default behavior for a notification, such as whether
                it should make a sound, vibrate, or use the device's LED indicator. This method allows you to
                specify a combination of default notification behaviors.

                Here are the values that cn be used `from kvdroid.jclass.androidx` module:

                `NotificationCompat().DEFAULT_SOUND`: Use the default notification sound.
                `NotificationCompat().DEFAULT_VIBRATE: Make the device vibrate.
                `NotificationCompat().DEFAULT_LIGHTS`: Use the device's LED indicator (if available).
                `NotificationCompat().DEFAULT_ALL`: Use all default behaviors (sound, vibration, and LED).
            `broadcast`: bool
                sends out a broadcast message to your app to perform an action when an action button is
                clicked or reply is sent from your apps notification
        :return: notification_manager
        """
        if not priority:
            priority = NotificationCompat().PRIORITY_HIGH
        if not defaults:
            defaults = NotificationCompat().DEFAULT_ALL
        if not java_class:
            java_class = python_act
        if not extras:
            extras = {"tap": ()}

        # use activity_class instead of java_class because notifications are meant to open
        # are meant to open the app when the content (not the action buttons) is tapped
        tap_pending_intent = _create_intent(extras.get("tap"), java_class, broadcast, KVDROID_TAP_ACTION_NOTIFICATION)
        builder = NotificationCompatBuilder(activity.getApplicationContext(), channel_id)
        _build_notification_content(
            auto_cancel, channel_id, tap_pending_intent, small_icon, small_icon_color, text, title, priority, defaults,
            builder
        )
        _build_notification_actions(
            action_title1, action_title2, action_title3, auto_cancel, key_text_reply, builder, extras, java_class,
            reply_title, broadcast
        )

        if big_picture:
            _set_big_picture(big_picture, builder)

        if large_icon:
            _set_large_icon(large_icon, builder)

        notification_manager = cast(NotificationManager(), activity.getSystemService(
            Context().NOTIFICATION_SERVICE
        ))
        # Create the NotificationChannel, but only on API 26+ because
        # the NotificationChannel class is new and not in the support library
        if VERSION().SDK_INT >= 26:
            _create_notification_channel(channel_id, channel_name, notification_manager)
        # notificationId is a unique int for each notification that you must define
        notification_manager.notify(ids, builder.build())
        return notification_manager


    def get_notification_reply_text(intent, key_text_reply):
        if remote_input := RemoteInput().getResultsFromIntent(intent):
            return remote_input.getCharSequence(key_text_reply)
except JavaException as e:
    raise JavaException(
        f"{e}\n"
        "Kvdroid: Androidx not Enabled, Cannot Import create_notification\n"
        "Use official kivy plyer module instead or enable androidx in buildozer.spec file"
    ) from e
