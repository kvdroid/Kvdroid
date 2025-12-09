"""
Basic Notification Module

This module provides core functionality for creating and managing Android notifications
in Python applications. It offers a simplified interface to Android's NotificationCompat
API, making it easy to create rich, interactive notifications with minimal code.

Notifications are messages that Android displays outside of your app's UI to provide
users with reminders, communication from other people, or other timely information from
your app. Users can tap the notification to open your app or take an action directly
from the notification.

Key Features:
    - Create notifications with customizable icons, titles, and text
    - Support for action buttons (up to 3) and inline reply functionality
    - Rich media support (large icons and big picture styles)
    - Progress indicators for ongoing tasks
    - Notification grouping and stacking
    - Full-screen notifications for high-priority alerts
    - Custom vibration patterns and LED colors
    - Lock screen visibility controls
    - Extract user reply text from notification interactions

Main Functions:
    create_notification():
        Creates and displays a notification with extensive customization options
        including visual styling, actions, and interaction handlers.

    get_notification_reply_text():
        Retrieves user text input from inline reply notifications, enabling
        quick responses without opening the app.

Usage:
    from kvdroid.tools.notification.basic import create_notification
    from kvdroid.tools import get_resource_identifier

    # Create a simple notification
    notification_manager = create_notification(
        small_icon=get_resource_identifier("icon", "drawable"),
        channel_id="messages",
        title="New Message",
        text="You have a new message from John",
        notification_id=1
    )

    # Create a notification with action buttons
    notification_manager = create_notification(
        small_icon=get_resource_identifier("icon", "drawable"),
        channel_id="messages",
        title="New Message",
        text="You have a new message",
        notification_id=2,
        action_title1="Mark as Read",
        action_title2="Reply",
        reply_title="Reply",
        key_text_reply="reply_key",
        extras={
            "action1": ("action", "mark_read"),
            "reply": ("action", "send_reply")
        }
    )

Note:
    - Requires a notification channel to be created first on Android SDK 26+
    - Use create_notification_channel() from kvdroid.tools.notification.channel
      before creating notifications
    - On Android 8.0+ (API 26), notifications must be posted to a valid channel
"""

__all__ = ("create_notification", "get_notification_reply_text", "Notification")

from typing import Union
from android import python_act  # NOQA
from kvdroid import activity
from kvdroid.jclass.android import Uri
from kvdroid.jclass.androidx import (
    NotificationCompat,
    NotificationCompatBuilder,
    NotificationManagerCompat,
    RemoteInput,
)
from kvdroid.jclass.java import InputStream
from kvdroid.tools.graphics import get_bitmap
from kvdroid.tools.notification.constants import (
    Default,
    Foreground,
    Priority,
    KVDROID_TAP_ACTION_NOTIFICATION,
)
from kvdroid.tools.notification.utils import (
    _create_intent,
    _build_notification_content,
    _build_notification_actions,
    _set_big_picture,
    _set_large_icon,
    Intent,
)
from kvdroid.tools.notification.styles import Style, Person
from kvdroid.tools.notification import Builder


class Notification(Builder):
    """
    A builder class for creating Android notifications with method chaining.

    This class provides a Pythonic interface to Android's NotificationCompat.Builder,
    allowing you to construct notifications with extensive customization through
    chainable methods. Each method returns self, enabling fluent API usage.

    The Notification class is the recommended way to create notifications, offering
    more flexibility and control than the legacy create_notification_old function.
    Use create_notification() to post the notification after building it.

    Args:
        channel_id (str): The notification channel ID. On Android 8.0+ (API 26),
            notifications must be posted to a valid channel. Create channels using
            create_notification_channel() from kvdroid.tools.notification.channel.

    Example:
        >>> from kvdroid.tools.notification.basic import Notification, create_notification
        >>> from kvdroid.tools import get_resource_identifier
        >>> from kvdroid.jclass.android import Color
        >>>
        >>> # Build a notification with method chaining
        >>> notification = (
        ...     Notification("messages")
        ...     .set_small_icon(get_resource_identifier("ic_notification", "drawable"))
        ...     .set_content_title("New Message")
        ...     .set_content_text("You have a new message")
        ...     .set_auto_cancel(True)
        ...     .set_color(Color().BLUE)
        ... )
        >>>
        >>> # Post the notification
        >>> manager = create_notification(1, notification)
    """

    __slots__ = ("builder",)

    def __init__(self, channel_id: str):
        """
        Initialize a notification builder.

        Args:
            channel_id (str): The notification channel ID used to categorize and
                manage notifications. Channels must be created before posting
                notifications on Android 8.0+ (API 26).
        """
        self.builder = NotificationCompatBuilder(activity, channel_id)

    def add_action(self, icon: int, title: str, intent):
        """
        Add an action button to the notification.

        Action buttons appear below the notification content and allow users to
        take specific actions without opening the app. Up to 3 action buttons
        can be added to a notification.

        Args:
            icon (int): Resource ID of the icon for the action button. Use
                get_resource_identifier("icon_name", "drawable") to get the ID.
            title (str): Text displayed on the action button.
            intent (Intent): Intent object from kvdroid.tools.notification that
                wraps a PendingIntent. The intent will be triggered when the
                button is tapped.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> from kvdroid.tools.notification.utils import Intent
            >>> intent = Intent()
            >>> intent.set_action("archive")
            >>> notification.add_action(icon_id, "Archive", intent)
        """
        self.builder.addAction(icon, title, intent)
        return self

    def add_person(self, person: Person):
        """
        Adds a person to the builder and returns the current instance of the class.

        This method allows adding a `Person` object to the builder while enabling
        method chaining by returning the instance of the class.

        :param person: The `Person` object to be added to the builder.
        :type person: Person
        :return: The instance of the current class.
        :rtype: type(self)
        """
        self.builder.addPerson(person)
        return self

    def build(self):
        """
        Build and return the notification object.

        This method finalizes the notification construction and returns the
        Android Notification object that can be posted using create_notification().

        Returns:
            Notification: The built Android notification object.

        Example:
            >>> notification = Notification("channel_id").set_content_title("Title")
            >>> built = notification.build()
            >>> manager.notify(1, built)
        """
        return self.builder.build()

    def set_auto_cancel(self, auto_cancel: bool):
        """
        Set whether the notification is automatically dismissed when tapped.

        When auto_cancel is True, tapping the notification will automatically
        dismiss it. This is the common behavior for most notifications.

        Args:
            auto_cancel (bool): True to automatically dismiss the notification
                when tapped, False to keep it visible.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> notification.set_auto_cancel(True)
        """
        self.builder.setAutoCancel(auto_cancel)
        return self

    def set_color(self, color: int):
        """
        Set the background color for the small icon.

        This color is used as the background for the small notification icon
        in the notification header on Android 5.0+ (API 21). It appears as a
        colored circle behind the icon.

        Args:
            color (int): The color value. Use Color class from kvdroid.jclass.android
                module, e.g., Color().BLUE or Color().rgb(0x00, 0xC8, 0x53).

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> from kvdroid.jclass.android import Color
            >>> notification.set_color(Color().BLUE)
        """
        self.builder.setColor(color)
        return self

    def set_colorized(self, colorized: bool):
        """
        Set whether to colorize the entire notification.

        When enabled, applies the notification color to the entire notification
        background instead of just the icon background.

        Args:
            colorized (bool): True to colorize the entire notification.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> notification.set_colorized(True)
        """
        self.builder.setColorized(colorized)
        return self

    def set_content_intent(self, intent: Intent):
        """
        Set the intent to launch when the notification is tapped.

        This determines what happens when the user taps the notification body
        (not the action buttons). Typically opens an activity in your app.

        Args:
            intent (Intent): Intent object from kvdroid.tools.notification that
                wraps a PendingIntent to launch when notification is tapped.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> from kvdroid.tools.notification.utils import Intent
            >>> intent = Intent()
            >>> intent.put_extra("key", "value")
            >>> notification.set_content_intent(intent)
        """
        self.builder.setContentIntent(intent.get_intent())
        return self

    def set_content_text(self, text: str):
        """
        Set the notification's body text.

        The text provides additional information related to the notification's
        title and helps users understand the purpose or context of the notification.

        Args:
            text (str): The notification body text.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> notification.set_content_text("You have a new message from John")
        """
        self.builder.setContentText(text)
        return self

    def set_content_title(self, title: str):
        """
        Set the notification's title.

        The title is a short, descriptive text displayed prominently at the top
        of the notification, providing context for the notification's content.

        Args:
            title (str): The notification title.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> notification.set_content_title("New Message")
        """
        self.builder.setContentTitle(title)
        return self

    def set_defaults(self, defaults: Default):
        """
        Set default notification behaviors (sound, vibration, LED).

        This method specifies which default notification behaviors to use, such as
        the default sound, vibration pattern, or LED indicator.

        Args:
            defaults (Default): Default behavior enum from kvdroid.tools.notification.constants.
                Options include: DEFAULT_SOUND, DEFAULT_VIBRATE, DEFAULT_LIGHTS, DEFAULT_ALL.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> from kvdroid.tools.notification.constants import Default
            >>> notification.set_defaults(Default.ALL)
        """
        self.builder.setDefaults(defaults.value)
        return self

    def set_delete_intent(self, intent: Intent):
        """
        Set the intent to launch when the notification is dismissed.

        This intent is triggered when the user dismisses the notification
        (swipes it away). Useful for cleanup or tracking dismissal actions.

        Args:
            intent (Intent): Intent object from kvdroid.tools.notification that
                wraps a PendingIntent to launch when notification is dismissed.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> from kvdroid.tools.notification.utils import Intent
            >>> delete_intent = Intent()
            >>> delete_intent.set_action("delete")
            >>> notification.set_delete_intent(delete_intent)
        """
        self.builder.setDeleteIntent(intent.get_intent())
        return self

    def set_foreground_service_behavior(self, behavior: Foreground):
        """
        Set the behavior for foreground service notifications.

        Controls how the notification behaves when associated with a foreground service.

        Args:
            behavior (Foreground): Foreground behavior enum from
                kvdroid.tools.notification.constants.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> from kvdroid.tools.notification.constants import Foreground
            >>> notification.set_foreground_service_behavior(Foreground.IMMEDIATE)
        """
        self.builder.setForegroundServiceBehavior(behavior.value)
        return self

    def set_full_screen_intent(self, intent: Intent, is_pending_intent: bool):
        """
        Set the intent to launch as a full-screen alert.

        When triggered, this notification will launch as a full-screen intent,
        useful for high-priority alerts like incoming calls or alarms that need
        immediate user attention.

        Args:
            intent (Intent): Intent object from kvdroid.tools.notification that
                wraps a PendingIntent to launch full-screen.
            is_pending_intent (bool): True if the intent is high priority and should
                launch immediately.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> from kvdroid.tools.notification.utils import Intent
            >>> full_screen_intent = Intent()
            >>> full_screen_intent.set_action("alarm")
            >>> notification.set_full_screen_intent(full_screen_intent, True)
        """
        self.builder.setFullScreenIntent(intent.get_intent(), is_pending_intent)
        return self

    def set_group(self, group_key: str):
        """
        Set the group key to group related notifications together.

        Notifications with the same group_key will be stacked together in the
        notification shade, helping organize related notifications.

        Args:
            group_key (str): A unique identifier for grouping notifications.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> notification.set_group("message_group")
        """
        self.builder.setGroup(group_key)
        return self

    def set_group_summary(self, is_group_summary: bool):
        """
        Set whether this notification is the summary for a group.

        When True, this notification acts as a summary for a group of notifications
        with the same group_key. The summary is displayed when notifications are
        stacked together.

        Args:
            is_group_summary (bool): True to make this the group summary notification.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> notification.set_group("messages").set_group_summary(True)
        """
        self.builder.setGroupSummary(is_group_summary)
        return self

    def set_large_icon(self, large_icon: int | str | object):
        """
        Set the large icon displayed alongside the notification content.

        The large_icon is an optional image displayed to the right of the
        notification text, typically larger than the small icon. It provides
        additional visual context or appeal.

        Args:
            large_icon (int | str | object): The large icon as a resource ID,
                file path string (e.g., "assets/image/icon.png"), or InputStream.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> notification.set_large_icon("assets/profile.png")
            >>> # or
            >>> notification.set_large_icon(get_resource_identifier("avatar", "drawable"))
        """
        bitmap = get_bitmap(large_icon)
        self.builder.setLargeIcon(bitmap)
        return self

    def set_lights(self, color: int, on_ms: int, off_ms: int):
        """
        Set the LED notification light pattern.

        Configures the device's LED indicator (if available) to blink with the
        specified color and timing pattern.

        Args:
            color (int): The LED color. Use Color class from kvdroid.jclass.android.
            on_ms (int): Duration in milliseconds the LED is on.
            off_ms (int): Duration in milliseconds the LED is off.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> from kvdroid.jclass.android import Color
            >>> notification.set_lights(Color().BLUE, 1000, 500)
        """
        self.builder.setLights(color, on_ms, off_ms)
        return self

    def set_number(self, number: int):
        """
        Set the number badge displayed on the notification icon.

        Shows a number badge on the notification, typically used to indicate
        the count of pending items, unread messages, or similar countable items.

        Args:
            number (int): The number to display.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> notification.set_number(5)  # Shows "5" badge
        """
        self.builder.setNumber(number)
        return self

    def set_ongoing(self, ongoing: bool):
        """
        Set whether the notification is ongoing (persistent).

        When True, the notification cannot be dismissed by swiping. Useful for
        persistent notifications like music players, active downloads, or
        foreground services.

        Args:
            ongoing (bool): True to make the notification persistent.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> notification.set_ongoing(True)
        """
        self.builder.setOngoing(ongoing)
        return self

    def set_only_alert_once(self, only_alert_once: bool):
        """
        Set whether to alert (sound, vibrate) only once for this notification.

        When True, the notification will only make sound and vibrate the first time
        it's posted. Updates to the notification won't trigger alerts again.

        Args:
            only_alert_once (bool): True to alert only on first notification.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> notification.set_only_alert_once(True)
        """
        self.builder.setOnlyAlertOnce(only_alert_once)
        return self

    def set_priority(self, priority: Priority):
        """
        Set the priority level of the notification.

        Priority determines how the notification is treated in terms of importance
        and visibility. Higher priority notifications are more prominent and may
        make sound or vibration.

        Priority levels (from kvdroid.tools.notification.constants.PRIORITY):
            - MIN: Least important, not shown unless user opens notification shade
            - LOW: Less prominent, no sound/vibration typically
            - DEFAULT: Regular notifications
            - HIGH: Prominent display, may make sound/vibration
            - MAX: Most important, displayed prominently with sound/vibration

        Args:
            priority (Priority): Priority level enum from constants.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> from kvdroid.tools.notification.constants import Priority
            >>> notification.set_priority(Priority.HIGH)
        """
        self.builder.setPriority(priority.value)
        return self

    def set_progress(self, max: int, progress: int, indeterminate: bool):
        """
        Set a progress bar in the notification.

        Displays a progress bar showing the completion status of an ongoing task
        like downloads, uploads, or processing operations.

        Args:
            max (int): The maximum progress value (e.g., 100 for percentage).
            progress (int): The current progress value (e.g., 45 for 45%).
            indeterminate (bool): True to show an indeterminate (spinning) progress
                bar when the completion time is unknown.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> # 45% progress
            >>> notification.set_progress(100, 45, False)
            >>> # Indeterminate progress
            >>> notification.set_progress(0, 0, True)
        """
        self.builder.setProgress(max, progress, indeterminate)
        return self

    def set_remote_input_history(self, history: list[str]):
        """
        Set the history of previous text inputs in reply notifications.

        Displays a list of previous text inputs in the notification, useful for
        showing conversation context in messaging notifications.

        Args:
            history (list[str]): A list of previous text inputs to display.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> notification.set_remote_input_history(["Hello!", "How are you?"])
        """
        self.builder.setRemoteInputHistory(history)
        return self

    def set_request_promote_ongoing(self, request_promote_ongoing: bool):
        """
        Request that the notification be promoted to ongoing status.

        Requests that the system promote this notification to an ongoing notification
        under certain conditions.

        Args:
            request_promote_ongoing (bool): True to request promotion to ongoing.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> notification.set_request_promote_ongoing(True)
        """
        self.builder.setRequestPromoteOngoing(request_promote_ongoing)
        return self

    def set_short_critical_text(self, short_critical_text: str):
        """
        Set short critical text for time-sensitive notifications.

        Sets brief text for critical, time-sensitive notifications that need
        immediate attention.

        Args:
            short_critical_text (str): Short critical message text.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> notification.set_short_critical_text("URGENT")
        """
        self.builder.setShortCriticalText(short_critical_text)
        return self

    def set_shortcut_id(self, shortcut_id: str):
        """
        Associate this notification with a shortcut ID.

        Links the notification to a sharing shortcut, enabling conversation
        shortcuts in the share sheet.

        Args:
            shortcut_id (str): The shortcut ID to associate with.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> notification.set_shortcut_id("conversation_john")
        """
        self.builder.setShortcutId(shortcut_id)
        return self

    def set_show_when(self, show_when: bool):
        """
        Set whether to show the timestamp in the notification.

        Controls whether the notification displays the time it was posted.

        Args:
            show_when (bool): True to show the timestamp.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> notification.set_show_when(True)
        """
        self.builder.setShowWhen(show_when)
        return self

    def set_silent(self, silent: bool):
        """
        Set whether the notification should be silent.

        When True, the notification will not make any sound or vibration,
        regardless of channel settings.

        Args:
            silent (bool): True to make the notification silent.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> notification.set_silent(True)
        """
        self.builder.setSilent(silent)
        return self

    def set_small_icon(self, icon: int):
        """
        Set the small icon displayed in the notification bar.

        The small icon appears at the top of the notification and in the status bar.
        This is a required field for notifications.

        Args:
            icon (int): Resource ID of the icon. Use get_resource_identifier("icon_name",
                "drawable") from kvdroid.tools to get the resource ID.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> from kvdroid.tools import get_resource_identifier
            >>> icon_id = get_resource_identifier("ic_notification", "drawable")
            >>> notification.set_small_icon(icon_id)
        """
        self.builder.setSmallIcon(icon)
        return self

    def set_sound(self, sound: int):
        """
        Set a custom notification sound.

        Plays the specified sound when the notification is posted. For Android 8.0+
        (API 26), custom sounds should preferably be set on the notification channel,
        but this method can be used for backward compatibility.

        Args:
            sound (int): Resource ID of the sound file. Use
                get_resource_identifier("sound_name", "raw") from kvdroid.tools
                to get the resource ID of a sound in your app's res/raw folder.

        Returns:
            Notification: Returns self for method chaining.

        Note:
            On Android 8.0+, channel sound settings take precedence over this setting.

        Example:
            >>> from kvdroid.tools import get_resource_identifier
            >>> sound_id = get_resource_identifier("notification_sound", "raw")
            >>> notification.set_sound(sound_id)
        """
        self.builder.setSound(
            Uri().parse(f"android.resource://{activity.getPackageName()}/{sound}")
        )
        return self

    def set_style(self, style: Style):
        """
        Set the notification style for rich content display.

        Applies a style to the notification for displaying rich content like
        large images (BigPictureStyle), expanded text (BigTextStyle), inbox-style
        lists (InboxStyle), or messaging conversations (MessagingStyle).

        Args:
            style (Style): A Style object from kvdroid.tools.notification.styles
                containing the notification style configuration.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> from kvdroid.tools.notification.styles import BigPictureStyle
            >>> big_picture_style = BigPictureStyle().set_big_picture("path/to/image.png")
            >>> notification.set_style(big_picture_style)
        """
        self.builder.setStyle(style.get_style())
        return self

    def set_sub_text(self, sub_text: str):
        """
        Set additional subtext displayed in the notification.

        Adds a third line of text below the title and content text, useful for
        displaying supplementary information.

        Args:
            sub_text (str): The subtext to display.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> notification.set_sub_text("2 hours ago")
        """
        self.builder.setSubText(sub_text)
        return self

    def set_ticker(self, ticker: str):
        """
        Set the ticker text for accessibility services.

        Sets text that is announced by accessibility services when the notification
        is posted. On older Android versions, this text scrolled across the status bar.

        Args:
            ticker (str): The ticker text.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> notification.set_ticker("New message received")
        """
        self.builder.setTicker(ticker)
        return self

    def set_timeout_after(self, timeout_after: int):
        """
        Set the notification to auto-dismiss after a specified duration.

        Automatically cancels the notification after the specified time period,
        even if the user hasn't interacted with it.

        Args:
            timeout_after (int): Time in milliseconds after which the notification
                will be automatically dismissed.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> notification.set_timeout_after(5000)  # Auto-dismiss after 5 seconds
        """
        self.builder.setTimeoutAfter(timeout_after)
        return self

    def set_uses_chronometer(self, uses_chronometer: bool):
        """
        Set whether to display a chronometer instead of timestamp.

        When True, displays a running timer counting up from the time set with
        set_when(), useful for showing elapsed time (e.g., call duration, recording time).

        Args:
            uses_chronometer (bool): True to show a chronometer instead of timestamp.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> import time
            >>> notification.set_when(int(time.time() * 1000)).set_uses_chronometer(True)
        """
        self.builder.setUsesChronometer(uses_chronometer)
        return self

    def set_vibrate(self, pattern: list[int]):
        """
        Set a custom vibration pattern for the notification.

        Configures the device to vibrate in a specific pattern when the notification
        is posted. The pattern alternates between vibrate and pause durations.

        Args:
            pattern (list[int]): List of integers representing vibration pattern
                in milliseconds. Format: [delay, vibrate, pause, vibrate, pause, ...]
                Example: [0, 250, 200, 250] means no delay, vibrate 250ms, pause 200ms,
                vibrate 250ms.

        Returns:
            Notification: Returns self for method chaining.

        Note:
            On Android 8.0+, vibration patterns should preferably be set on the
            notification channel for consistency.

        Example:
            >>> notification.set_vibrate([0, 250, 200, 250])
        """
        self.builder.setVibrate(pattern)
        return self

    def set_visibility(self, visibility):
        """
        Set the visibility level on the lock screen.

        Controls what notification content is shown when the device is locked.

        Visibility levels (use NotificationCompat constants):
            - VISIBILITY_PUBLIC: Show full notification content on lock screen
            - VISIBILITY_PRIVATE: Show basic info but hide content on lock screen
            - VISIBILITY_SECRET: Don't show any notification on lock screen

        Args:
            visibility (int): Visibility constant from NotificationCompat.

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> from kvdroid.jclass.androidx import NotificationCompat
            >>> notification.set_visibility(NotificationCompat().VISIBILITY_PRIVATE)
        """
        self.builder.setVisibility(visibility)
        return self

    def set_when(self, when: int):
        """
        Set the timestamp displayed in the notification.

        Sets the time value shown in the notification. This can be used to show
        when an event occurred or as the base time for a chronometer.

        Args:
            when (int): Time in milliseconds since epoch (Unix timestamp * 1000).

        Returns:
            Notification: Returns self for method chaining.

        Example:
            >>> import time
            >>> notification.set_when(int(time.time() * 1000))
        """
        self.builder.setWhen(when)
        return self


def create_notification(notification_id: int, notification: Notification):
    """
    Post a notification to the system notification manager.

    This is the recommended way to create and display notifications. It takes a
    Notification object built using the Notification class's builder methods and
    posts it to the Android notification manager.

    The notification will appear in the device's notification shade and can include
    rich content, action buttons, reply functionality, and various customization
    options configured through the Notification builder.

    Args:
        notification_id (int): A unique integer identifier for this notification.
            This ID is used to update or cancel the notification later. Using the
            same ID will replace an existing notification.
        notification (Notification): The Notification object to post, created using
            the Notification class builder pattern.

    Returns:
        NotificationManagerCompat: The notification manager instance that posted
            the notification. Use this to update or cancel notifications:
            - manager.notify(id, notification) to update
            - manager.cancel(id) to cancel

    Example:
        >>> from kvdroid.tools.notification.basic import Notification, create_notification
        >>> from kvdroid.tools import get_resource_identifier
        >>>
        >>> # Build a notification with the builder pattern
        >>> notification = (
        ...     Notification("messages")
        ...     .set_small_icon(get_resource_identifier("ic_notification", "drawable"))
        ...     .set_content_title("New Message")
        ...     .set_content_text("You have a new message from John")
        ...     .set_auto_cancel(True)
        ... )
        >>>
        >>> # Post the notification
        >>> manager = create_notification(1, notification)
        >>>
        >>> # Later, update the notification
        >>> updated_notification = (
        ...     Notification("messages")
        ...     .set_small_icon(get_resource_identifier("ic_notification", "drawable"))
        ...     .set_content_title("Messages")
        ...     .set_content_text("2 new messages")
        ... )
        >>> manager.notify(1, updated_notification.build())
        >>>
        >>> # Cancel the notification
        >>> manager.cancel(1)

    Note:
        - A notification channel must be created before posting notifications on
          Android 8.0+ (API 26). Use create_notification_channel() from
          kvdroid.tools.notification.channel.
        - The notification_id allows you to manage notifications: use the same ID
          to update an existing notification or cancel it with manager.cancel(id).
        - This function is preferred over create_notification_old() for new code
          as it provides more flexibility and follows modern Android patterns.
    """
    notification_manager = getattr(NotificationManagerCompat(), "from")(activity)
    # notificationId is a unique int for each notification that you must define
    notification_manager.notify(notification_id, notification.build())
    return notification_manager


def cancel_notification(notification_id: int):
    """Cancel a notification by ID."""
    getattr(NotificationManagerCompat(), "from")(activity).cancel(notification_id)


def get_notification_reply_text(intent, key_text_reply):
    """
    Extracts user text input from a notification reply action.

    When a notification includes an inline reply action (using key_text_reply and reply_title
    in create_notification), users can type a response directly in the notification. This
    function retrieves that text input from the intent received when the reply action is
    triggered.

    This is commonly used in messaging apps to allow users to respond to messages without
    opening the app. The reply text is extracted from the RemoteInput results attached to
    the intent.

    Parameters:
        intent:
            The intent received from the notification action. This is typically obtained
            from the Android activity's onNewIntent or broadcast receiver when a reply
            action is triggered. The intent contains the RemoteInput results with the
            user's text input.
        key_text_reply (str):
            The unique key that was used when creating the notification's reply action.
            This must match the key_text_reply parameter passed to create_notification().
            It's used to identify and retrieve the specific text input from the RemoteInput
            results.

    Returns:
        str or None:
            Returns the user's text input as a string if reply text is found in the intent.
            Returns None if no RemoteInput results exist in the intent or if the specified
            key is not found in the results.

    Example:
        >>> from kvdroid.tools.notification.basic import get_notification_reply_text
        >>> # In your activity or broadcast receiver, when reply action is triggered:
        >>> def on_notification_action(intent):
        ...     reply_text = get_notification_reply_text(intent, "reply_key")
        ...     if reply_text:
        ...         print(f"User replied: {reply_text}")
        ...         # Process the reply (send message, etc.)
        ...     else:
        ...         print("No reply text found")

    Note:
        - This function should be called when handling notification action intents
        - The key_text_reply must match exactly with the one used in create_notification
        - Returns None if the intent doesn't contain RemoteInput results (e.g., if the
          user tapped a regular action button instead of using the reply field)
    """
    if remote_input := RemoteInput().getResultsFromIntent(intent):
        return remote_input.getCharSequence(key_text_reply)
    return None
