"""
Notification Constants Module

This module defines action identifiers and intent extra keys used throughout the kvdroid
notification system. These constants provide a standardized way to identify different
notification interactions and pass data between notifications and the application.

The constants are prefixed with the application's package name to ensure uniqueness and
prevent conflicts with other apps or system components.

Constants:
    Action Identifiers (used to identify notification interaction types):
        KVDROID_REPLY_ACTION_NOTIFICATION:
            Action identifier for inline reply actions. Used when a user responds to a
            notification using the inline reply feature. This action is triggered when
            the user submits text through the notification's reply input field.

        KVDROID_ACTION_1_NOTIFICATION:
            Action identifier for the first action button (action_title1 parameter).
            Used to identify when the user taps the first custom action button on a
            notification.

        KVDROID_ACTION_2_NOTIFICATION:
            Action identifier for the second action button (action_title2 parameter).
            Used to identify when the user taps the second custom action button on a
            notification.

        KVDROID_ACTION_3_NOTIFICATION:
            Action identifier for the third action button (action_title3 parameter).
            Used to identify when the user taps the third custom action button on a
            notification.

        KVDROID_TAP_ACTION_NOTIFICATION:
            Action identifier for notification content tap. Used when a user taps on
            the notification body (not on action buttons). This typically opens the
            main activity of the app.

    Intent Extra Keys (used to pass metadata in notification intents):
        EXTRA_NOTIFICATION_ID:
            Key for passing the notification ID as an intent extra. Used to identify
            which notification triggered an action, allowing the app to perform
            notification-specific operations like canceling or updating.

        EXTRA_CHANNEL_ID:
            Key for passing the channel ID as an intent extra. Used to identify which
            notification channel the notification belongs to.

Usage:
    These constants are primarily used internally by the notification module but can
    also be used in broadcast receivers or activities to handle notification actions.

    Example - Handling notification actions in a broadcast receiver:
        from kvdroid.tools.notification.constants import (
            KVDROID_ACTION_1_NOTIFICATION,
            KVDROID_REPLY_ACTION_NOTIFICATION,
            EXTRA_NOTIFICATION_ID
        )
        from kvdroid.tools.notification.basic import get_notification_reply_text

        def on_notification_action(intent):
            action = intent.getAction()
            notification_id = intent.getIntExtra(EXTRA_NOTIFICATION_ID, -1)

            if action == KVDROID_ACTION_1_NOTIFICATION:
                # Handle first action button tap
                print(f"Action 1 tapped on notification {notification_id}")

            elif action == KVDROID_REPLY_ACTION_NOTIFICATION:
                # Handle inline reply
                reply_text = get_notification_reply_text(intent, "reply_key")
                print(f"User replied: {reply_text}")

Note:
    All action identifiers are automatically prefixed with the app's package name
    (obtained via activity.getPackageName()) to ensure uniqueness across the system.
"""

__all__ = (
    "KVDROID_REPLY_ACTION_NOTIFICATION",
    "KVDROID_ACTION_1_NOTIFICATION",
    "KVDROID_ACTION_2_NOTIFICATION",
    "KVDROID_ACTION_3_NOTIFICATION",
    "KVDROID_TAP_ACTION_NOTIFICATION",
    "EXTRA_NOTIFICATION_ID",
    "EXTRA_CHANNEL_ID",
    "Importance",
    "Default",
    "Foreground",
    "Priority",
    "PendingIntentFlag",
)

from enum import IntFlag
from kvdroid import activity


KVDROID_REPLY_ACTION_NOTIFICATION = (
    f"{activity.getPackageName()}.KVDROID_REPLY_ACTION_NOTIFICATION"
)
KVDROID_ACTION_1_NOTIFICATION = (
    f"{activity.getPackageName()}.KVDROID_ACTION_1_NOTIFICATION"
)
KVDROID_ACTION_2_NOTIFICATION = (
    f"{activity.getPackageName()}.KVDROID_ACTION_2_NOTIFICATION"
)
KVDROID_ACTION_3_NOTIFICATION = (
    f"{activity.getPackageName()}.KVDROID_ACTION_3_NOTIFICATION"
)
KVDROID_TAP_ACTION_NOTIFICATION = (
    f"{activity.getPackageName()}.KVDROID_TAP_ACTION_NOTIFICATION"
)


EXTRA_NOTIFICATION_ID = "kvdroid_notification_id"
EXTRA_CHANNEL_ID = "kvdroid_channel_id"


class Importance(IntFlag):
    DEFAULT = 3
    HIGH = 4
    LOW = 2
    MAX = 5
    MIN = 1
    NONE = 0
    UNSPECIFIED = -1000


class Default(IntFlag):
    ALL = -1
    LIGHTS = 4
    SOUNDS = 1
    VIBRATE = 2


class Foreground(IntFlag):
    SERVICE_DEFAULT = 0
    SERVICE_DEFERRED = 2
    SERVICE_IMMEDIATE = 1


class Priority(IntFlag):
    DEFAULT = 0
    HIGH = 1
    LOW = -1
    MAX = 2
    MIN = -2


class PendingIntentFlag(IntFlag):
    FLAG_ALLOW_UNSAFE_IMPLICIT_INTENT = 16777216
    FLAG_CANCEL_CURRENT = 268435456
    FLAG_IMMUTABLE = 67108864
    FLAG_MUTABLE = 33554432
    FLAG_NO_CREATE = 536870912
    FLAG_ONE_SHOT = 1073741824
    FLAG_UPDATE_CURRENT = 134217728
