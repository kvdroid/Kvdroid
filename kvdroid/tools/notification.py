"""
Androidx Notification
=====================
"""

from typing import Union
from jnius import cast, JavaException  # NOQA
from android import python_act  # NOQA
from kvdroid import Logger, activity
from kvdroid.cast import cast_object
from kvdroid.jclass.android import BitmapFactory
from kvdroid.jclass.java import InputStream
from kvdroid.tools import get_resource
from kvdroid.tools.graphics import bitmap_to_drawable

BitmapFactory = BitmapFactory()

try:
    from kvdroid.jclass.androidx import (
        ContextCompat,
        NotificationCompatBuilder,
        NotificationCompat,
        NotificationCompatActionBuilder,
        RemoteInputBuilder,
        NotificationCompatBigPictureStyle,
        NotificationBigTextStyle
    )
    from kvdroid.jclass.android import (
        Intent,
        Context,
        PendingIntent,
        NotificationManager,
        Notification,
        NotificationChannel,
        VERSION
    )
    from kvdroid.jclass.java.lang import String, System


    def _create_intent(extras, java_class):
        intent = Intent(activity.getApplication().getApplicationContext(), java_class)
        if extras:
            intent.putExtra(*extras)
        intent.setFlags(Intent().FLAG_ACTIVITY_CLEAR_TOP | Intent().FLAG_ACTIVITY_SINGLE_TOP)
        intent.setAction(Intent().ACTION_MAIN)
        intent.addCategory(Intent().CATEGORY_LAUNCHER)
        return (
            PendingIntent().getActivity(
                activity.getApplication().getApplicationContext(),
                0,
                intent,
                PendingIntent().FLAG_MUTABLE,
            )
            if VERSION().SDK_INT >= 31
            else PendingIntent().getActivity(
                activity.getApplication().getApplicationContext(),
                0,
                intent,
                PendingIntent().FLAG_UPDATE_CURRENT
                | Notification().FLAG_AUTO_CANCEL,
            )
        )


    def _create_notification_channel(channel_id, channel_name, notification_manager):
        importance: int = NotificationManager().IMPORTANCE_HIGH
        channel = NotificationChannel(String(channel_id), String(channel_name), importance)
        channel.setDescription("notification")
        # Register the channel with the system; you can't change the importance
        # or other notification behaviors after this
        notification_manager.createNotificationChannel(channel)


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
            builder
    ):
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
        builder.setStyle(NotificationBigTextStyle(instantiate=True).bigText(String(text)).setBigContentTitle(text))

    def _build_notification_actions(
            action_title1,
            action_title2,
            action_title3,
            auto_cancel,
            key_text_reply,
            builder,
            reply_title,
            pending_intent,
    ):
        if action_title1:
            builder.addAction(
                get_resource("mipmap").icon, cast_object("charSequence", String(action_title1)), pending_intent
            )

        if action_title2:
            builder.addAction(
                get_resource("mipmap").icon, cast_object("charSequence", String(action_title2)), pending_intent
            )

        if action_title3:
            builder.addAction(
                get_resource("mipmap").icon, cast_object("charSequence", String(action_title3)), pending_intent
            )

        if reply_title:
            builder.addAction(
                NotificationCompatActionBuilder(
                    get_resource("mipmap").icon,
                    String(reply_title),
                    pending_intent
                ).addRemoteInput(
                    RemoteInputBuilder(String(key_text_reply)).setLabel(String(reply_title)).build()
                ).build()
            ).setAutoCancel(auto_cancel)

    def _set_big_picture(big_picture, builder):
        large_picture = NotificationCompatBigPictureStyle(instantiate=True)
        if isinstance(big_picture, int):
            large_picture.bigPicture(BitmapFactory.decodeResource(activity.getResources(), big_picture))
        elif isinstance(big_picture, str):
            large_picture.bigPicture(BitmapFactory.decodeFile(big_picture))
        else:
            large_picture.bigPicture(BitmapFactory.decodeStream(big_picture))
        builder.setStyle(large_picture)

    def _set_large_icon(large_icon, builder):
        if isinstance(large_icon, int):
            builder.setLargeIcon(BitmapFactory.decodeResource(activity.getResources(), large_icon))
        elif isinstance(large_icon, str):
            builder.setLargeIcon(BitmapFactory.decodeFile(large_icon))
        else:
            builder.setLargeIcon(BitmapFactory.decodeStream(large_icon))


    def create_notification(
            small_icon: int,
            channel_id: str,
            title: str,
            text: str,
            ids: int,
            channel_name: str,
            large_icon: Union[int, str, InputStream()] = 0,
            big_picture: Union[int, str, InputStream()] = 0,
            action_title1: str = None,
            action_title2: str = None,
            action_title3: str = None,
            key_text_reply: str = None,
            reply_title: str = None,
            auto_cancel: bool = True,
            extras: tuple = None,
            small_icon_color: int = 0,
            java_class=python_act,
            priority: int = None,
            defaults: int = None
    ):  # sourcery no-metrics
        if not priority:
            priority = NotificationCompat().PRIORITY_HIGH
        if not defaults:
            defaults = NotificationCompat().DEFAULT_ALL
        # Create the NotificationChannel, but only on API 26+ because
        # the NotificationChannel class is new and not in the support library
        notification_manager = cast(NotificationManager(), activity.getSystemService(
            Context().NOTIFICATION_SERVICE
        ))
        if VERSION().SDK_INT >= 26:
            _create_notification_channel(channel_id, channel_name, notification_manager)
        pending_intent = _create_intent(extras=extras, java_class=java_class)
        builder = NotificationCompatBuilder(activity.getApplication().getApplicationContext(), channel_id)
        _build_notification_content(
            auto_cancel, channel_id, pending_intent, small_icon, small_icon_color, text, title, priority, defaults,
            builder
        )
        _build_notification_actions(
            action_title1, action_title2, action_title3, auto_cancel, key_text_reply, builder, reply_title,
            pending_intent
        )

        if big_picture:
            _set_big_picture(big_picture, builder)

        if large_icon:
            _set_large_icon(large_icon, builder)

        # notificationId is a unique int for each notification that you must define
        notification_manager.notify(ids, builder.build())
except JavaException as error:
    Logger.error(
        f"{str(error)}\n"
        "Kvdroid: Androidx not Enabled, Cannot Import create_notification\n"
        "Use official kivy plyer module instead or enable androidx in buildozer.spec file"
    )
