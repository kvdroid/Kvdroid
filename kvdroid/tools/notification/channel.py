"""
Notification Channel Management Module.

This module provides Python wrappers for creating and managing Android
notification channels (API 26+). A notification channel represents a category
of notifications with common characteristics such as importance, sound,
vibration pattern, and visual settings. Users can customize these settings per
channel in the system settings.

Highlights:
    - Builder-like fluent API via the ``NotificationChannel`` class
    - Configure importance, sound, vibration, badges, lights, and more
    - Group channels and support conversation threads (API 30+)
    - Simple ``create_notification_channel()`` helper to register a channel

Recommended usage (fluent API):
    from kvdroid.tools.notification.channel import NotificationChannel, create_notification_channel
    from kvdroid.tools.notification.constants import IMPORTANCE

    channel = (
        NotificationChannel("messages", "Messages", IMPORTANCE.HIGH)
        .set_description("Notifications for new messages")
        .enable_vibration(True)
        .set_vibration_pattern([0, 300, 200, 300])
        .enable_lights(True)
        .set_show_badge(True)
    )
    create_notification_channel(channel)

Backward compatibility:
    A legacy helper ``create_notification_channel_old`` is still available for
    apps that used the previous keyword-argument style. Prefer the fluent API
    shown above for new code.

API Level:
    Notification channels are supported on API 26+ (Android Oreo). On older
    versions the helper will be a no-op (or return None in legacy function).
"""

__all__ = ("NotificationChannel", "create_notification_channel")

from kvdroid import activity, require_api
from kvdroid.jclass.android import (
    NotificationManager,
    NotificationChannel as NotificationChannelJava,
    Uri,
    AudioAttributes,
    AudioAttributesBuilder,
)
from kvdroid.tools.notification.constants import Importance
from kvdroid.tools.vibration import VibrationEffect


@require_api(">=", 26)
class NotificationChannel:
    """Fluent builder for Android notification channels (API 26+).

    Use this class to configure channel properties via chained setter methods
    and then register it using ``create_notification_channel(channel)``.

    Args:
        channel_id (str): Unique identifier for the channel. Cannot be changed once created.
        channel_name (str): Human-readable name shown in system settings.
        importance (Importance): Importance level controlling visibility and alerting.

    Common setters:
        - ``set_group(group_id: str)``
        - ``set_description(description: str)``
        - ``set_conversation_id(parent_channel_id: str, conversation_id: int)`` (API 30+)
        - ``set_light_color(light_color: int)``
        - ``set_lockscreen_visibility(lock_screen_visibility: int)``
        - ``set_name(name: str)``
        - ``set_vibration_effect(vibration_effect: VibrationEffect)`` (API 35+)
        - ``set_vibration_pattern(vibration_pattern: list[int])``
        - ``set_sound(sound: int)``
        - ``set_show_badge(show_badge: bool)``
        - ``enable_lights(enable_lights: bool)``
        - ``enable_vibration(enable_vibration: bool)``

    Example:
        >>> from kvdroid.tools.notification.channel import NotificationChannel, create_notification_channel
        >>> from kvdroid.tools.notification.constants import Importance
        >>>
        >>> channel = (
        ...     NotificationChannel("alerts", "Alerts", Importance.HIGH)
        ...     .set_description("Important alerts and warnings")
        ...     .set_show_badge(True)
        ...     .enable_vibration(True)
        ... )
        >>> create_notification_channel(channel)
    """

    __slots__ = ("channel",)

    def __init__(self, channel_id: str, channel_name: str, importance: Importance):
        """Initialize a new Android notification channel wrapper.

        Args:
            channel_id (str): Unique, immutable identifier for the channel.
            channel_name (str): Human‑readable name shown in system settings.
            importance (Importance): Importance level controlling alerting/visibility.
        """
        self.channel = NotificationChannelJava(
            channel_id, channel_name, importance.value
        )

    def set_group(self, group_id: str):
        """Assign this channel to a notification group.

        Args:
            group_id (str): The ID of the previously created `NotificationChannelGroup`.

        Returns:
            NotificationChannel: This instance for method chaining.
        """
        self.channel.setGroup(group_id)
        return self

    def set_description(self, description: str):
        """Set the user‑visible description of this channel.

        Args:
            description (str): Human‑readable description shown in system settings.

        Returns:
            NotificationChannel: This instance for method chaining.
        """
        self.channel.setDescription(description)
        return self

    @require_api(">=", 30)
    def set_conversation_id(self, parent_channel_id: str, conversation_id: int):
        """Associate a conversation with this channel (API 30+).

        Args:
            parent_channel_id (str): The parent channel ID hosting the conversation.
            conversation_id (int): App‑defined unique conversation identifier.

        Returns:
            NotificationChannel: This instance for method chaining.
        """
        self.channel.setConversationId(parent_channel_id, conversation_id)
        return self

    def set_light_color(self, light_color: int):
        """Set the LED light color for notifications posted to this channel.

        Args:
            light_color (int): ARGB color integer (e.g., 0xFFFF0000 for red).

        Returns:
            NotificationChannel: This instance for method chaining.
        """
        self.channel.setLightColor(light_color)
        return self

    def set_lockscreen_visibility(self, lock_screen_visibility: int):
        """Control how notifications are shown on the lock screen.

        Args:
            lock_screen_visibility (int): One of `Notification.VISIBILITY_*`.

        Returns:
            NotificationChannel: This instance for method chaining.
        """
        self.channel.setLockscreenVisibility(lock_screen_visibility)
        return self

    def set_name(self, name: str):
        """Update the user‑visible name of the channel.

        Args:
            name (str): New name shown in system settings.

        Returns:
            NotificationChannel: This instance for method chaining.

        Note:
            Many channel properties (including name) may not take effect after
            creation on some Android versions. Users can change these in settings.
        """
        self.channel.setName(name)
        return self

    @require_api(">=", 35)
    def set_vibration_effect(self, vibration_effect: VibrationEffect):
        """Set a rich `VibrationEffect` for notifications in this channel (API 35+).

        Args:
            vibration_effect (VibrationEffect): Instance from `kvdroid.tools.vibration`.

        Returns:
            NotificationChannel: This instance for method chaining.
        """
        self.channel.setVibrationEffect(vibration_effect.get_effect())
        return self

    def set_vibration_pattern(self, vibration_pattern: list[int]):
        """Set a custom vibration pattern for the channel.

        Args:
            vibration_pattern (list[int]): Alternating on/off durations in ms.

        Returns:
            NotificationChannel: This instance for method chaining.
        """
        self.channel.setVibrationPattern(vibration_pattern)
        return self

    def set_sound(self, sound: int):
        """Set a custom notification sound resource for this channel.

        Args:
            sound (int): Android raw resource ID (e.g., from `R.raw`).

        Returns:
            NotificationChannel: This instance for method chaining.
        """
        self.channel.setSound(
            Uri().parse(f"android.resource://{activity.getPackageName()}/{sound}"),
            AudioAttributesBuilder()
            .setContentType(AudioAttributes().CONTENT_TYPE_SONIFICATION)
            .setUsage(AudioAttributes().USAGE_NOTIFICATION)
            .build(),
        )
        return self

    def set_show_badge(self, show_badge: bool):
        """Enable or disable app icon badges for this channel.

        Args:
            show_badge (bool): True to allow badges, False to disable.

        Returns:
            NotificationChannel: This instance for method chaining.
        """
        self.channel.setShowBadge(show_badge)
        return self

    def enable_lights(self, enable_lights: bool):
        """Enable or disable notification LED lights for this channel.

        Args:
            enable_lights (bool): True to enable; False to disable.

        Returns:
            NotificationChannel: This instance for method chaining.
        """
        self.channel.enableLights(enable_lights)
        return self

    def enable_vibration(self, enable_vibration: bool):
        """Enable or disable vibration for this channel.

        Args:
            enable_vibration (bool): True to enable; False to disable.

        Returns:
            NotificationChannel: This instance for method chaining.
        """
        self.channel.enableVibration(enable_vibration)
        return self


@require_api(">=", 26)
def create_notification_channel(channel: NotificationChannel):
    """Register the given ``NotificationChannel`` with the system (API 26+).

    Args:
        channel (NotificationChannel): Configured channel instance built via the
            fluent API in this module.

    Returns:
        NotificationManager: The system notification manager used to create the channel.

    Note:
        Once a channel is created, most properties cannot be changed
        programmatically; users control them in system settings.
    """
    notification_manager = activity.getSystemService(NotificationManager()._class)
    notification_manager.createNotificationChannel(channel.channel)
    return notification_manager
