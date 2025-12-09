"""
KVDroid Notification Package

This package provides a comprehensive and user-friendly interface for creating and managing
Android notifications in Python applications built with Kivy and KivMob. It abstracts the
complexity of Android's notification system, offering simplified functions for common
notification tasks while maintaining support for advanced features.

The notification package is organized into several modules:
    - basic: Core notification creation and reply handling functions
    - channel: Notification channel management (Android 8.0+)
    - constants: Action identifiers and intent extra keys
    - utils: Internal utility functions for notification building
    - fullscreen: Full-screen notification support for high-priority alerts

Key Features:
    - Simple notification creation with rich content support
    - Notification channels for user-customizable notification categories
    - Action buttons (up to 3 per notification)
    - Inline reply functionality for quick responses
    - Large icons and big picture styles for rich media
    - Progress indicators for ongoing tasks
    - Notification grouping and stacking
    - Full-screen notifications for alarms and calls
    - Custom sounds, vibration patterns, and LED colors
    - Lock screen visibility controls

Exported Functions:
    create_notification(small_icon, channel_id, title, text, notification_id, **kwargs):
        Creates and displays a notification with extensive customization options.
        Supports action buttons, inline replies, progress bars, and rich media content.

    get_notification_reply_text(intent, key_text_reply):
        Extracts user text input from notification inline reply actions.
        Used to retrieve responses submitted through notification reply fields.

Exported Constants:
    Action Identifiers:
        KVDROID_TAP_ACTION_NOTIFICATION - Notification body tap action
        KVDROID_ACTION_1_NOTIFICATION - First action button
        KVDROID_ACTION_2_NOTIFICATION - Second action button
        KVDROID_ACTION_3_NOTIFICATION - Third action button
        KVDROID_REPLY_ACTION_NOTIFICATION - Inline reply action

    Intent Extra Keys:
        EXTRA_NOTIFICATION_ID - Key for notification ID in intents
        EXTRA_CHANNEL_ID - Key for channel ID in intents

Quick Start:
    1. Create a notification channel (Android 8.0+):
        >>> from kvdroid.tools.notification.channel import NotificationChannel, create_notification_channel
        >>> from kvdroid.tools.notification.constants import IMPORTANCE
        >>>
        >>> channel = (
        ...     NotificationChannel("messages", "Messages", IMPORTANCE.HIGH)
        ...     .set_description("Notifications for new messages")
        ...     .enable_vibration(True)
        ...     .set_show_badge(True)
        ... )
        >>> create_notification_channel(channel)

    2. Create and display a notification using the builder API:
        >>> from kvdroid.tools.notification import Notification, create_notification
        >>> from kvdroid.tools import get_resource_identifier
        >>>
        >>> notification = (
        ...     Notification("messages")
        ...     .set_small_icon(get_resource_identifier("ic_notification", "drawable"))
        ...     .set_content_title("New Message")
        ...     .set_content_text("You have a new message")
        ...     .set_auto_cancel(True)
        ... )
        >>> manager = create_notification(1, notification)

    3. Create a notification with intents and actions:
        >>> from kvdroid.tools.notification import Notification, Intent, create_notification
        >>> from android import python_act
        >>>
        >>> tap_intent = Intent(("msg_id", "123"), python_act._class, "TAP_ACTION", "messages", 1)
        >>> action_intent = Intent(("action", "archive"), python_act._class, "ACTION_1", "messages", 1)
        >>>
        >>> notification = (
        ...     Notification("messages")
        ...     .set_small_icon(get_resource_identifier("ic_notification", "drawable"))
        ...     .set_content_title("New Message")
        ...     .set_content_text("John: How are you?")
        ...     .set_content_intent(tap_intent)
        ...     .add_action(0, "Archive", action_intent)
        ... )
        >>> manager = create_notification(2, notification)

    4. Handle notification actions in your activity or broadcast receiver:
        >>> from kvdroid.tools.broadcast import BroadcastReceiver
        >>> from android.activity import bind as activity_bind
        >>>
        >>> def on_notification_action(intent):
        ...     if extras := intent.getExtras():
        ...         if msg_id := extras.getString("msg_id"):
        ...             print(f"Notification tapped: {msg_id}")
        ...         elif action := extras.getString("action"):
        ...             print(f"Action pressed: {action}")
        >>>
        >>> activity_bind(on_new_intent=on_notification_action)
        >>> br = BroadcastReceiver(
        ...     callback=lambda _, intent: on_notification_action(intent),
        ...     actions=["TAP_ACTION", "ACTION_1"],
        ...     use_intent_action=False
        ... )
        >>> br.start()

Note:
    - Notification channels must be created before posting notifications on Android 8.0+
    - Once created, channel settings (importance, sound, etc.) can only be changed by users
    - Use unique notification IDs to display multiple notifications simultaneously
    - Action buttons are limited to 3 per notification
    - For detailed parameter documentation, see individual function docstrings

See Also:
    - kvdroid.tools.notification.basic: Main notification functions
    - kvdroid.tools.notification.channel: Channel management
    - kvdroid.tools.notification.constants: Action and extra key constants
"""

__all__ = ("Builder",)

from abc import ABC, abstractmethod


class Builder(ABC):
    """Abstract base class for builder pattern implementations.

    This class defines the interface for builder objects that construct
    Android notification components.
    """

    @abstractmethod
    def build(self):
        """Build and return the Android notification component.

        Returns:
            object: The constructed Android notification component.
        """
        pass
