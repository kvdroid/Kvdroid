from jnius import cast, JavaException
from android import python_act
from kvdroid.cast import cast_object
try:
    from kvdroid import (
        Context,
        Intent,
        PendingIntent,
        activity,
        NotificationCompatBuilder,
        System,
        NotificationCompat,
        get_resource,
        RemoteInputBuilder,
        NotificationCompatActionBuilder,
        NotificationCompatBigPictureStyle,
        BitmapFactory,
        NotificationManager,
        VERSION,
        String, Logger
)

    def create_notification(
            small_icon: int, channel_id: str, title: str, text: str, ids: int, channel_name: str, big_picture: int,
            action_title1: str = "", action_title2: str = "", action_title3: str = "", key_text_reply: str = "",
            reply_title: str = "",
            expandable: bool = False, set_large_icon: bool = False, add_action_button2: bool = False,
            add_action_button3: bool = False, auto_cancel: bool = True, add_action_button1: bool = False,
            set_reply: bool = False
    ):
        intent = Intent(activity.getApplication().getApplicationContext(), python_act)
        intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP)
        intent.setAction(Intent.ACTION_MAIN)
        intent.addCategory(Intent.CATEGORY_LAUNCHER)
        pendingIntent = PendingIntent.getActivity(activity.getApplication().getApplicationContext(), 0, intent, 0)
        # Create the NotificationChannel, but only on API 26+ because
        # the NotificationChannel class is new and not in the support library
        if VERSION.SDK_INT >= 26:
            from kvdroid import NotificationChannel
            importance: int = NotificationManager.IMPORTANCE_HIGH
            channel = NotificationChannel(String(channel_id), String(channel_name), importance)
            channel.setDescription("notification")
            # Register the channel with the system; you can't change the importance
            # or other notification behaviors after this
            notificationManager = cast(NotificationManager, activity.getSystemService(
                    Context.NOTIFICATION_SERVICE
                ))
            notificationManager.createNotificationChannel(channel)

        builder = NotificationCompatBuilder(activity.getApplication().getApplicationContext(), channel_id)
        builder.setSmallIcon(small_icon)
        builder.setContentTitle(String(title))
        builder.setContentText(String(text))
        # Set the intent that will fire when the user taps the notification
        builder.setContentIntent(pendingIntent)
        builder.setWhen(System.currentTimeMillis())
        builder.setChannelId(String(channel_id))
        builder.setPriority(NotificationCompat.PRIORITY_HIGH)
        builder.setDefaults(NotificationCompat.DEFAULT_ALL)
        builder.setAutoCancel(auto_cancel)
        if add_action_button1:
            builder.addAction(
                get_resource("mipmap").icon, cast_object("charSequence", String(action_title1)), pendingIntent
            )

        if add_action_button2:
            builder.addAction(
                get_resource("mipmap").icon, cast_object("charSequence", String(action_title2)), pendingIntent
            )

        if add_action_button3:
            builder.addAction(
                get_resource("mipmap").icon, cast_object("charSequence", String(action_title3)), pendingIntent
            )

        if set_reply:
            # remoteInput = RemoteInputBuilder(String(key_text_reply))
            # remoteInput.setLabel(String(reply_title))
            # remoteInput.build()
            builder.addAction(
                NotificationCompatActionBuilder(
                    get_resource("mipmap").icon, String(reply_title), pendingIntent).addRemoteInput(
                    RemoteInputBuilder(String(key_text_reply)).setLabel(
                        String(reply_title)).build()
                ).build()
            ).setAutoCancel(auto_cancel)

        if expandable:
            bigPicture = NotificationCompatBigPictureStyle()
            bigPicture.bigPicture(BitmapFactory.decodeResource(activity.getResources(), big_picture))
            builder.setStyle(bigPicture)

        if set_large_icon:
            builder.setLargeIcon(BitmapFactory.decodeResource(activity.getResources(), big_picture))

        notification = cast(NotificationManager, activity.getSystemService(
                    Context.NOTIFICATION_SERVICE
                ))

        # notificationId is a unique int for each notification that you must define
        notification.notify(ids, builder.build())
except JavaException:
    Logger.error(
        "Kvdroid: Androidx not Enabled, Cannot Import create_notification\n"
        "Use official kivy plyer module instead or enable androidx in buildozer.spec file"
    )