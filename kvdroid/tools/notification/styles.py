"""Android Notification Styles Module.

This module provides Python wrapper classes for various Android notification styles,
enabling rich notification displays with different layouts and interaction patterns.

The module follows the Builder pattern for constructing complex notification styles
and provides abstractions over AndroidX NotificationCompat and Android Notification APIs.

Available Notification Styles:
    - MessagingStyle: Chat and messaging applications (API 24+)
    - BigTextStyle: Large text content display (API 16+)
    - BigPictureStyle: Image-based notifications (API 16+)
    - InboxStyle: Multiple line items list (API 16+)
    - MediaStyle: Media playback controls (API 21+)
    - CallStyle: Incoming and ongoing call notifications (API 31+)
    - ProgressStyle: Progress indicators and tracking (API 36+)

API Level Compatibility:
    - Most basic styles (BigTextStyle, BigPictureStyle, InboxStyle) work from API 16+
    - MessagingStyle requires API 24+ (historic messages require API 26+)
    - MediaStyle requires API 21+ (remote playback info requires API 31+)
    - CallStyle requires API 31+
    - ProgressStyle requires API 36+
    - Person objects require API 28+

Note:
    When using AndroidX NotificationCompat classes, backward compatibility is provided
    automatically for devices running older Android versions where possible.
"""

__all__ = (
    "Person",
    "MessagingStyle",
    "BigTextStyle",
    "BigPictureStyle",
    "InboxStyle",
    "CallStyle",
    "MediaStyle",
    "ProgressPoint",
    "ProgressSegment",
    "ProgressStyle",
    "Style",
)

from abc import ABC, abstractmethod

from kvdroid import require_api
from kvdroid.jclass.android import (
    PersonBuilder,
    Icon,
    NotificationCallStyle,
    NotificationProgressStyle,
    NotificationProgressStylePoint,
    NotificationProgressStyleSegment,
)
from kvdroid.jclass.androidx import (
    NotificationCompatMessagingStyle,
    NotificationCompatMessagingStyleMessage,
    NotificationBigTextStyle,
    NotificationCompatBigPictureStyle,
    NotificationCompatInboxStyle,
    MediaStyleNotificationHelperMediaStyle,
)
from kvdroid.jclass.java import List
from kvdroid.tools.graphics import get_bitmap
from kvdroid.tools.notification import Builder


class Style(ABC):
    """Abstract base class for notification style implementations.

    All notification style classes inherit from this base class and must
    implement the get_style() method to return an Android notification style object.
    """

    @abstractmethod
    def get_style(self):
        """Build and return the Android notification style object.

        Returns:
            object: The constructed Android notification style object.
        """
        pass


@require_api(">=", 28)
class Person(Builder):
    """Represents a person for use in MessagingStyle and CallStyle notifications.

    Person objects are used to identify participants in messaging and call notifications,
    providing metadata such as name, icon, and importance.

    API Level: Requires API 28+ (Android P)

    Attributes (conceptual):
        name (str): Display name of the person.
        icon (int | str | object): Icon resource as drawable ID (int), file path (str),
            or java.io.InputStream object for loading from streams.
        bot (bool): Whether this person is a bot. Default is False.
        important (bool): Whether this person is important. Default is False.
        key (str): Unique identifier for this person. Optional.

    Example:
        >>> person = (
        ...     Person()
        ...     .set_name("John Doe")
        ...     .set_icon("/path/to/avatar.png")
        ...     .set_important(True)
        ... )
        >>> android_person = person.build()
    """

    __slots__ = ("builder",)

    def __init__(self):
        """Initialize a Person builder.

        Note:
            This constructor takes no parameters. Use the fluent setter methods
            like ``set_name()``, ``set_icon()``, ``set_bot()``, etc., and then
            call ``build()`` to obtain the Android ``Person`` instance.
        """
        self.builder = PersonBuilder(instantiate=True)

    def set_bot(self, bot: bool):
        """Set whether this person is a bot.

        Args:
            bot: True if this person is a bot, False otherwise.

        Returns:
            Person: This Person instance for method chaining.
        """
        self.builder.setBot(bot)
        return self

    def set_icon(self, icon: int | str | object):
        """Set the icon for this person.

        Args:
            icon: Icon resource as drawable ID (int), file path (str),
                or java.io.InputStream object.

        Returns:
            Person: This Person instance for method chaining.
        """
        bitmap = get_bitmap(icon)
        icon = Icon().createWithBitmap(bitmap)
        self.builder.setIcon(icon)
        return self

    def set_important(self, important: bool):
        """Set whether this person is important.

        Important persons may be displayed with special styling in notifications.

        Args:
            important: True if this person is important, False otherwise.

        Returns:
            Person: This Person instance for method chaining.
        """
        self.builder.setImportant(important)
        return self

    def set_key(self, key: str):
        """Set a unique identifier for this person.

        The key is used to identify this person across app restarts and
        should remain consistent for the same individual.

        Args:
            key: Unique identifier string for this person.

        Returns:
            Person: This Person instance for method chaining.
        """
        self.builder.setKey(key)
        return self

    def set_name(self, name: str):
        """Set the display name for this person.

        Args:
            name: The name to display for this person in notifications.

        Returns:
            Person: This Person instance for method chaining.
        """
        self.builder.setName(name)
        return self

    def set_uri(self, uri: str):
        """Set the URI associated with this person.

        The URI can be used to link to more information about the person,
        such as a contact profile or chat thread.

        Args:
            uri: URI string associated with this person.

        Returns:
            Person: This Person instance for method chaining.
        """
        self.builder.setUri(uri)
        return self

    def build(self):
        """Build an Android Person object.

        Constructs a native Android Person object using PersonBuilder,
        converting the icon to a bitmap and setting all configured attributes.

        Returns:
            android.app.Person: The constructed Android Person object.

        API Level: Requires API 28+
        """
        return self.builder.build()


class MessagingStyle(Style):
    """Notification style for messaging and chat applications.

    Displays messages in a conversation format with support for multiple participants,
    message history, and proper attribution of each message to its sender.

    Attributes:
        user (Person): The current user (displayed as "You" in the notification).

    Example:
        >>> me = Person().set_name("Me").set_icon("/path/to/my_avatar.png")
        >>> alice = Person().set_name("Alice").set_icon("/path/to/alice_avatar.png")
        >>> style = MessagingStyle(user=me)
        >>> style.add_message("Hello!", 1234567890000, alice)
        >>> style.add_message("Hi Alice!", 1234567891000, me)
    """

    __slots__ = ("style",)

    def __init__(self, user: Person):
        """Initialize a MessagingStyle.

        Args:
            user: Person object representing the current user.
        """
        self.style = NotificationCompatMessagingStyle(user.build())

    def add_message(self, text: str, timestamp: int, person: Person):
        """Add a message to the notification.

        Messages are displayed in chronological order in the notification.

        Args:
            text: The message text content.
            timestamp: Message timestamp in milliseconds since epoch (Unix time).
            person: Person object representing the message sender.

        Returns:
            MessagingStyle: This MessagingStyle instance for method chaining.

        API Level: Requires API 24+
        """
        self.style.addMessage(text, timestamp, person.build())
        return self

    def add_historic_message(self, text: str, timestamp: int, person: Person):
        """Add a historic message to the notification.

        Historic messages are displayed separately from recent messages,
        providing context for the conversation without triggering notifications.

        Args:
            text: The message text content.
            timestamp: Message timestamp in milliseconds since epoch (Unix time).
            person: Person object representing the message sender.

        Returns:
            MessagingStyle: This MessagingStyle instance for method chaining.

        API Level: Requires API 26+
        """
        message = NotificationCompatMessagingStyleMessage(
            text, timestamp, person.build()
        )
        self.style.addHistoricMessage(message)
        return self

    def get_style(self):
        """Build the MessagingStyle notification style.

        Creates a NotificationCompat.MessagingStyle with all messages and historic messages.

        Returns:
            NotificationCompat.MessagingStyle: The constructed messaging style.
        """
        return self.style


class BigTextStyle(Style):
    """Notification style for displaying large amounts of text.

    Shows expanded text content in notifications, useful for email previews,
    long messages, or detailed information that doesn't fit in standard notifications.

    API Level: Requires API 16+ (Android Jelly Bean)

    Attributes:
        big_text (str): The large text content to display when notification is expanded.
        big_content_title (str): Optional title shown when notification is expanded.
        summary_text (str): Optional summary text shown when notification is expanded.

    Example:
        >>> style = (
        ...     BigTextStyle()
        ...     .big_text("This is a very long message that needs more space...")
        ...     .set_big_content_title("Email from John")
        ...     .set_summary_text("2 new messages")
        ... )
    """

    __slots__ = ("style",)

    def __init__(self):
        """Initialize a BigTextStyle.

        Note:
            This constructor takes no parameters. Configure content using the
            fluent methods like ``big_text()``, ``set_big_content_title()``, and
            ``set_summary_text()``.
        """
        self.style = NotificationBigTextStyle(instantiate=True)

    def big_text(self, big_text: str):
        """Set the large text content to display when notification is expanded.

        Args:
            big_text: The large text content. This text will be displayed
                when the user expands the notification.

        Returns:
            BigTextStyle: This BigTextStyle instance for method chaining.
        """
        self.style.bigText(big_text)
        return self

    def set_big_content_title(self, big_content_title: str):
        """Set the title to show when notification is expanded.

        This title replaces the notification's main content title when expanded.

        Args:
            big_content_title: The title text to show in expanded view.

        Returns:
            BigTextStyle: This BigTextStyle instance for method chaining.
        """
        self.style.setBigContentTitle(big_content_title)
        return self

    def set_summary_text(self, summary_text: str):
        """Set summary text to show when notification is expanded.

        The summary text appears below the big text content in the expanded view.

        Args:
            summary_text: The summary text to display.

        Returns:
            BigTextStyle: This BigTextStyle instance for method chaining.
        """
        self.style.setSummaryText(summary_text)
        return self

    def get_style(self):
        """Build the BigTextStyle notification style.

        Returns:
            NotificationCompat.BigTextStyle: The constructed big text style.

        API Level: Requires API 16+
        """
        return self.style


class BigPictureStyle(Style):
    """Notification style for displaying large images.

    Shows an expanded image in notifications, ideal for photo sharing apps,
    image messages, or visual content that needs prominence.

    API Level: Requires API 16+ (Android Jelly Bean)
    Content Description: Requires API 31+ (Android S)
    Show Big Picture When Collapsed: Requires API 31+ (Android S)

    Example:
        >>> style = (
        ...     BigPictureStyle()
        ...     .big_picture("/path/to/photo.jpg")
        ...     .set_big_content_title("Photo from Alice")
        ...     .set_content_description("Sunset over mountains")
        ...     .show_big_picture_when_collapsed(True)
        ... )
    """

    __slots__ = ("style",)

    def __init__(self):
        """Initialize a BigPictureStyle.

        Note:
            This constructor takes no parameters. Configure images and text using
            fluent methods like ``big_picture()``, ``big_large_icon()``,
            ``set_big_content_title()``, ``set_content_description()``, and
            ``set_summary_text()``.
        """
        self.style = NotificationCompatBigPictureStyle(instantiate=True)

    def big_picture(self, big_picture: int | str | object):
        """Set the main image to display in the notification.

        Args:
            big_picture: Main image as drawable ID (int), file path (str),
                or java.io.InputStream object.

        Returns:
            BigPictureStyle: This BigPictureStyle instance for method chaining.
        """
        self.style.bigPicture(get_bitmap(big_picture))
        return self

    def big_large_icon(self, big_large_icon: int | str | object):
        """Set the large icon to show when notification is expanded.

        This icon replaces the small notification icon when the notification
        is expanded, providing a larger visual element.

        Args:
            big_large_icon: Large icon as drawable ID (int), file path (str),
                or java.io.InputStream object.

        Returns:
            BigPictureStyle: This BigPictureStyle instance for method chaining.
        """
        self.style.bigLargeIcon(get_bitmap(big_large_icon))
        return self

    def set_big_content_title(self, big_content_title: str):
        """Set the title to show when notification is expanded.

        This title replaces the notification's main content title when expanded.

        Args:
            big_content_title: The title text to show in expanded view.

        Returns:
            BigPictureStyle: This BigPictureStyle instance for method chaining.
        """
        self.style.setBigContentTitle(big_content_title)
        return self

    def set_content_description(self, big_content_description: str):
        """Set accessibility description for the image.

        This description is used by accessibility services to describe
        the image to users with visual impairments.

        Args:
            big_content_description: Accessibility description of the image.

        Returns:
            BigPictureStyle: This BigPictureStyle instance for method chaining.

        API Level: Requires API 31+
        """
        self.style.setContentDescription(big_content_description)
        return self

    def set_summary_text(self, summary_text: str):
        """Set summary text to show when notification is expanded.

        The summary text appears below the image in the expanded view.

        Args:
            summary_text: The summary text to display.

        Returns:
            BigPictureStyle: This BigPictureStyle instance for method chaining.
        """
        self.style.setSummaryText(summary_text)
        return self

    def show_big_picture_when_collapsed(self, show_big_picture_when_collapsed: bool):
        """Control whether to show the big picture when notification is collapsed.

        When enabled, the image is shown even in the collapsed notification view.

        Args:
            show_big_picture_when_collapsed: True to show image in collapsed view,
                False to only show when expanded.

        Returns:
            BigPictureStyle: This BigPictureStyle instance for method chaining.

        API Level: Requires API 31+
        """
        self.style.showBigPictureWhenCollapsed(show_big_picture_when_collapsed)
        return self

    def get_style(self):
        """Build the BigPictureStyle notification style.

        Returns:
            NotificationCompat.BigPictureStyle: The constructed big picture style.

        API Level:
            - Base functionality: API 16+
            - Content description: API 31+
            - Show big picture when collapsed: API 31+
        """
        return self.style


class InboxStyle(Style):
    """Notification style for displaying multiple lines of text.

    Shows a list of text lines in notifications, useful for email inbox summaries,
    lists of notifications, or any content that benefits from a line-by-line format.

    API Level: Requires API 16+ (Android Jelly Bean)

    Example:
        >>> style = (
        ...     InboxStyle()
        ...     .add_line("Email 1: Meeting tomorrow")
        ...     .add_line("Email 2: Project update")
        ...     .add_line("Email 3: Lunch invitation")
        ...     .set_big_content_title("3 new emails")
        ...     .set_summary_text("john@example.com")
        ... )
    """

    __slots__ = ("style",)

    def __init__(self):
        """Initialize an InboxStyle.

        Note:
            This constructor takes no parameters. Add lines and configure titles
            using ``add_line()``, ``set_big_content_title()``, and
            ``set_summary_text()``.
        """
        self.style = NotificationCompatInboxStyle(instantiate=True)

    def add_line(self, line: str):
        """Add a line of text to the inbox notification.

        Lines are displayed in the order they are added. Up to 7 lines
        are typically shown in the expanded notification view.

        Args:
            line: A line of text to add to the inbox display.

        Returns:
            InboxStyle: This InboxStyle instance for method chaining.
        """
        self.style.addLine(line)
        return self

    def set_big_content_title(self, big_content_title: str):
        """Set the title to show when notification is expanded.

        This title replaces the notification's main content title when expanded.

        Args:
            big_content_title: The title text to show in expanded view.

        Returns:
            InboxStyle: This InboxStyle instance for method chaining.
        """
        self.style.setBigContentTitle(big_content_title)
        return self

    def set_summary_text(self, summary_text: str):
        """Set summary text to show when notification is expanded.

        The summary text appears below the inbox lines in the expanded view.

        Args:
            summary_text: The summary text to display.

        Returns:
            InboxStyle: This InboxStyle instance for method chaining.
        """
        self.style.setSummaryText(summary_text)
        return self

    def get_style(self):
        """Build the InboxStyle notification style.

        Returns:
            NotificationCompat.InboxStyle: The constructed inbox style.

        API Level: Requires API 16+
        """
        return self.style


class MediaStyle(Style):
    """Notification style for media playback controls.

    Displays media playback controls and information in notifications,
    used by music players, video players, and other media applications.

    API Level: Requires API 21+ (Android Lollipop)
    Remote Playback Info: Requires API 31+ (Android S)
    Example:
        >>> style = MediaStyle(media_session_token)
        >>> style.set_show_actions_in_compact_view(0)
        >>> style.set_show_actions_in_compact_view(1)
        >>> style.set_show_actions_in_compact_view(2)
        >>> style.set_remote_playback_info("Living Room TV", icon_id, intent)
    """

    __slots__ = ("style",)

    def __init__(self, media_session):
        """Initialize a MediaStyle.

        Args:
            media_session: MediaSession token for the active media session.
        """
        self.style = MediaStyleNotificationHelperMediaStyle(media_session)

    def set_show_actions_in_compact_view(self, action: int):
        """Set an action index to show in compact notification view.

        In the collapsed notification view, only a limited number of actions
        can be displayed (typically up to 3). This method specifies which
        action indices should be shown. Call this method multiple times to
        show multiple actions.

        Args:
            action: Zero-based index of the notification action to show
                in compact view (e.g., 0 for first action, 1 for second).

        Returns:
            MediaStyle: This MediaStyle instance for method chaining.
        """
        self.style.setShowActionsInCompactView(action)
        return self

    def set_remote_playback_info(
        self, device_name: str, icon_resource: int, chip_intent: object
    ):
        """Set information about remote playback device.

        Displays a chip in the notification showing that media is playing
        on a remote device (e.g., a TV or speaker).

        Args:
            device_name: Name of the remote playback device (e.g., "Living Room TV").
            icon_resource: Drawable resource ID for the device icon.
            chip_intent: PendingIntent triggered when the device chip is clicked.

        Returns:
            MediaStyle: This MediaStyle instance for method chaining.

        API Level: Requires API 31+
        """
        self.style.setRemotePlaybackInfo(device_name, icon_resource, chip_intent)
        return self

    def get_style(self):
        """Build the MediaStyle notification style.

        Returns:
            androidx.media.app.NotificationCompat.MediaStyle: The constructed media style.

        API Level:
            - Base functionality: API 21+
            - Remote playback info: API 31+
        """
        return self.style


@require_api(">=", 31)
class CallStyle(Style):
    """Notification style for incoming and ongoing call notifications.

    Displays call notifications with caller information, call actions (answer/decline/hang up),
    and optional verification indicators. Provides a rich, full-screen capable UI for calls.

    API Level: Requires API 31+ (Android S)

    Example:
        >>> caller = Person().set_name("Alice").set_icon("/path/to/avatar.png")
        >>> style = (
        ...     CallStyle.for_incoming_call(caller, decline_intent, answer_intent)
        ...     .set_is_video(True)
        ...     .set_answer_button_color_hint(0xFF00FF00)
        ...     .set_decline_button_color_hint(0xFFFF0000)
        ...     .set_verification_text("Verified")
        ... )
    """

    style = None

    def __init__(self):
        """Initialize a CallStyle.

        Note:
            Do not instantiate directly. Use one of the factory classmethods:
            ``for_incoming_call()``, ``for_ongoing_call()``, or ``for_screening_call()``.
            Then configure optional properties via fluent setters.
        """

        if not self.style:
            raise TypeError(
                "CallStyle must be initialized with for_incoming_call() or for_ongoing_call() or for_screening_call()"
            )

    @classmethod
    def for_incoming_call(cls, person: Person, decline_intent, answer_intent):
        """Create a CallStyle for an incoming call notification.

        Displays an incoming call with answer and decline actions.

        Args:
            person: Person object representing the caller.
            decline_intent: PendingIntent triggered when decline button is pressed.
            answer_intent: PendingIntent triggered when answer button is pressed.

        Returns:
            CallStyle: A new CallStyle instance configured for incoming calls.

        API Level: Requires API 31+
        """
        cls.style = NotificationCallStyle().forIncomingCall(
            person.build(), decline_intent, answer_intent
        )
        return cls()

    @classmethod
    def for_ongoing_call(cls, person, hang_up_intent):
        """Create a CallStyle for an ongoing call notification.

        Displays an active call with hang up action.

        Args:
            person: Person object representing the other party in the call.
            hang_up_intent: PendingIntent triggered when hang up button is pressed.

        Returns:
            CallStyle: A new CallStyle instance configured for ongoing calls.

        API Level: Requires API 31+
        """
        cls.style = NotificationCallStyle().forOngoingCall(
            person.build(), hang_up_intent
        )
        return cls()

    @classmethod
    def for_screening_call(cls, person, hang_up_intent, answer_intent):
        """Create a CallStyle for a call screening notification.

        Displays a call being screened with hang up and answer actions.

        Args:
            person: Person object representing the caller being screened.
            hang_up_intent: PendingIntent triggered when hang up button is pressed.
            answer_intent: PendingIntent triggered when answer button is pressed.

        Returns:
            CallStyle: A new CallStyle instance configured for screening calls.

        API Level: Requires API 31+
        """
        cls.style = NotificationCallStyle().forScreeningCall(
            person.build(), hang_up_intent, answer_intent
        )
        return cls()

    def set_answer_button_color_hint(self, answer_button_color_hint: int):
        """Set the color hint for the answer button.

        Args:
            answer_button_color_hint: ARGB color integer for the answer button
                (e.g., 0xFF00FF00 for green).

        Returns:
            CallStyle: This CallStyle instance for method chaining.
        """
        self.style.setAnswerButtonColorHint(answer_button_color_hint)
        return self

    def set_decline_button_color_hint(self, decline_button_color_hint: int):
        """Set the color hint for the decline button.

        Args:
            decline_button_color_hint: ARGB color integer for the decline button
                (e.g., 0xFFFF0000 for red).

        Returns:
            CallStyle: This CallStyle instance for method chaining.
        """
        self.style.setDeclineButtonColorHint(decline_button_color_hint)
        return self

    def set_is_video(self, is_video: bool):
        """Set whether this is a video call.

        Video calls may be displayed with different styling or icons.

        Args:
            is_video: True if this is a video call, False for audio only.

        Returns:
            CallStyle: This CallStyle instance for method chaining.
        """
        self.style.setIsVideo(is_video)
        return self

    def set_verification_icon(self, verification_icon: int | str | object):
        """Set the verification status icon.

        The verification icon indicates whether the caller's identity
        has been verified (e.g., showing a checkmark for verified callers).

        Args:
            verification_icon: Icon as drawable ID (int), file path (str),
                or java.io.InputStream object.

        Returns:
            CallStyle: This CallStyle instance for method chaining.
        """
        bitmap = get_bitmap(verification_icon)
        icon = Icon().createWithBitmap(bitmap)
        self.style.setVerificationIcon(icon)
        return self

    def set_verification_text(self, verification_text: str):
        """Set the verification status text.

        The verification text describes the caller's verification status
        (e.g., "Verified", "Spam Risk", etc.).

        Args:
            verification_text: Text describing verification status.

        Returns:
            CallStyle: This CallStyle instance for method chaining.
        """
        self.style.setVerificationText(verification_text)
        return self

    def get_style(self):
        """Build the CallStyle notification style.

        Returns:
            Notification.CallStyle: The constructed call style.

        API Level: Requires API 31+
        """
        return self.style


class ProgressSegment:
    """Represents a colored segment in a ProgressStyle notification.

    Used to display different colored segments along the progress indicator,
    useful for showing multiple phases or stages of progress.

    API Level: Requires API 36+ (Android V)

    Attributes:
        length (int): Length of the segment in progress units.
        color (int): Color of the segment as ARGB integer.
        id (int): Optional unique identifier for this segment.
    """

    __slots__ = ("segment",)

    def __init__(self, length: int):
        """Initialize a ProgressSegment.

        Args:
            length: Length of the segment in progress units.
            color: Color of the segment as ARGB integer (e.g., 0xFFFF0000 for red).
            id: Optional unique identifier for this segment.
        """
        self.segment = NotificationProgressStyleSegment(length)

    def set_color(self, color: int):
        """Set the color for this progress segment.

        Args:
            color: ARGB color integer for the segment (e.g., 0xFFFF0000 for red).

        Returns:
            ProgressSegment: This ProgressSegment instance for method chaining.
        """
        self.segment.setColor(color)
        return self

    def set_id(self, id: int):
        """Set a unique identifier for this segment.

        Args:
            id: Unique identifier integer for this segment.

        Returns:
            ProgressSegment: This ProgressSegment instance for method chaining.
        """
        self.segment.setId(id)
        return self

    def get_segment(self):
        """Get the native Android ProgressSegment object.

        Returns:
            Notification.ProgressStyle.Segment: The native Android segment object.
        """
        return self.segment


@require_api(">=", 36)
class ProgressPoint:
    """Represents a colored point marker in a ProgressStyle notification.

    Used to mark specific positions along the progress indicator,
    useful for showing milestones or important events.

    API Level: Requires API 36+ (Android V)
    """

    __slots__ = ("point",)

    def __init__(self, position: int):
        """Initialize a ProgressPoint.

        Args:
            position: Position of the point along the progress indicator.
        """
        self.point = NotificationProgressStylePoint(position)

    def set_color(self, color: int):
        """Set the color for this progress point marker.

        Args:
            color: ARGB color integer for the point (e.g., 0xFF00FF00 for green).

        Returns:
            ProgressPoint: This ProgressPoint instance for method chaining.
        """
        self.point.setColor(color)
        return self

    def set_id(self, id: int):
        """Set a unique identifier for this point.

        Args:
            id: Unique identifier integer for this point.

        Returns:
            ProgressPoint: This ProgressPoint instance for method chaining.
        """
        self.point.setId(id)
        return self

    def get_point(self):
        """Get the native Android ProgressPoint object.

        Returns:
            Notification.ProgressStyle.Point: The native Android point object.
        """
        return self.point


class ProgressStyle(Style):
    """Notification style for displaying progress indicators.

    Shows a progress bar in notifications with support for colored segments,
    milestone markers, and custom icons. Useful for downloads, uploads, or
    any long-running operations that need progress tracking.

    API Level: Requires API 36+ (Android V)

    Attributes:
        progress (int): Current progress value (0-100 for percentage, or custom range).
        progress_segments (list[ProgressSegment]): Optional colored segments along the progress bar.
        progress_points (list[ProgressPoint]): Optional milestone markers along the progress bar.
        progress_indeterminate (bool): Show indeterminate progress (no specific value). Default False.
        styled_by_progress (bool): Apply styling based on progress value. Default True.
        tracker_icon (int | str | object): Optional icon that tracks the progress position as drawable ID (int),
            file path (str), or java.io.InputStream object.
        start_icon (int | str | object): Optional icon shown at the start as drawable ID (int),
            file path (str), or java.io.InputStream object.
        end_icon (int | str | object): Optional icon shown at the end as drawable ID (int),
            file path (str), or java.io.InputStream object.

    Example:
        >>> segments = [
        ...     ProgressSegment(30).set_color(0xFFFF0000),  # Red segment
        ...     ProgressSegment(40).set_color(0xFF00FF00),  # Green segment
        ...     ProgressSegment(30).set_color(0xFF0000FF),  # Blue segment
        ... ]
        >>> style = ProgressStyle(
        ...     progress=75,
        ...     progress_segments=segments,
        ...     tracker_icon="/path/to/icon.png",
        ...     styled_by_progress=True
        ... )
    """

    __slots__ = (
        "progress",
        "progress_segments",
        "progress_points",
        "progress_indeterminate",
        "styled_by_progress",
        "tracker_icon",
        "start_icon",
        "end_icon",
    )

    def __init__(
        self,
        progress: int,
        progress_segments: list[ProgressSegment] = None,
        progress_points: list[ProgressPoint] = None,
        progress_indeterminate: bool = False,
        styled_by_progress: bool = True,
        tracker_icon: int | str | object = None,
        start_icon: int | str | object = None,
        end_icon: int | str | object = None,
    ):
        """Initialize a ProgressStyle.

        Args:
            progress: Current progress value (typically 0-100).
            progress_segments: Optional list of ProgressSegment objects for colored sections.
            progress_points: Optional list of ProgressPoint objects for milestone markers.
            progress_indeterminate: Show indeterminate progress (spinner-like). Default False.
            styled_by_progress: Apply styling based on progress value. Default True.
            tracker_icon: Optional icon as drawable ID (int), file path (str), or java.io.InputStream object
                that moves with progress position.
            start_icon: Optional icon as drawable ID (int), file path (str), or java.io.InputStream object
                shown at the start of progress bar.
            end_icon: Optional icon as drawable ID (int), file path (str), or java.io.InputStream object
                shown at the end of progress bar.
        """
        self.progress = progress
        self.progress_segments = progress_segments
        self.progress_points = progress_points
        self.progress_indeterminate = progress_indeterminate
        self.styled_by_progress = styled_by_progress
        self.tracker_icon = tracker_icon
        self.start_icon = start_icon
        self.end_icon = end_icon

        self.style = NotificationProgressStyle()

    def add_progress_point(self, point: ProgressPoint):
        """Add a single progress point marker to the progress bar.

        Args:
            point: ProgressPoint object representing a milestone marker.

        Returns:
            ProgressStyle: This ProgressStyle instance for method chaining.
        """
        self.style.addProgressPoint(point.get_point())
        return self

    def add_progress_segment(self, segment: ProgressSegment):
        """Add a single progress segment to the progress bar.

        Args:
            segment: ProgressSegment object representing a colored segment.

        Returns:
            ProgressStyle: This ProgressStyle instance for method chaining.
        """
        self.style.addProgressSegment(segment.get_segment())
        return self

    def set_progress(self, progress: int):
        """Set the current progress value.

        Args:
            progress: Current progress value (typically 0-100 for percentage).

        Returns:
            ProgressStyle: This ProgressStyle instance for method chaining.
        """
        self.style.setProgress(progress)
        return self

    def set_progress_end_icon(self, end_icon: int | str | object):
        """Set the icon to display at the end of the progress bar.

        Args:
            end_icon: Icon as drawable ID (int), file path (str),
                or java.io.InputStream object.

        Returns:
            ProgressStyle: This ProgressStyle instance for method chaining.
        """
        bitmap = get_bitmap(end_icon)
        icon = Icon().createWithBitmap(bitmap)
        self.style.setProgressEndIcon(icon)
        return self

    def set_progress_indeterminate(self, indeterminate: bool):
        """Set whether progress is indeterminate.

        Indeterminate progress displays an animated indicator without
        showing a specific progress value (like a spinner).

        Args:
            indeterminate: True for indeterminate progress, False for determinate.

        Returns:
            ProgressStyle: This ProgressStyle instance for method chaining.
        """
        self.style.setProgressIndeterminate(indeterminate)
        return self

    def set_progress_point(self, points: list[ProgressPoint]):
        """Set all progress point markers at once.

        This replaces any existing progress points with the provided list.

        Args:
            points: List of ProgressPoint objects representing milestone markers.

        Returns:
            ProgressStyle: This ProgressStyle instance for method chaining.
        """
        points = [point.get_point() for point in points]
        self.style.setProgressPoints(List().of(points))
        return self

    def set_progress_segment(self, segments: list[ProgressSegment]):
        """Set all progress segments at once.

        This replaces any existing progress segments with the provided list.

        Args:
            segments: List of ProgressSegment objects representing colored segments.

        Returns:
            ProgressStyle: This ProgressStyle instance for method chaining.
        """
        segments = [segment.get_segment() for segment in segments]
        self.style.setProgressSegments(List().of(segments))
        return self

    def set_progress_start_icon(self, start_icon: int | str | object):
        """Set the icon to display at the start of the progress bar.

        Args:
            start_icon: Icon as drawable ID (int), file path (str),
                or java.io.InputStream object.

        Returns:
            ProgressStyle: This ProgressStyle instance for method chaining.
        """
        bitmap = get_bitmap(start_icon)
        icon = Icon().createWithBitmap(bitmap)
        self.style.setProgressStartIcon(icon)
        return self

    def set_progress_tracker_icon(self, tracker_icon: int | str | object):
        """Set the icon that tracks along with the progress position.

        This icon moves along the progress bar as progress advances,
        providing a visual indicator of the current position.

        Args:
            tracker_icon: Icon as drawable ID (int), file path (str),
                or java.io.InputStream object.

        Returns:
            ProgressStyle: This ProgressStyle instance for method chaining.
        """
        bitmap = get_bitmap(tracker_icon)
        icon = Icon().createWithBitmap(bitmap)
        self.style.setProgressTrackerIcon(icon)
        return self

    def set_styled_by_progress(self, styled_by_progress: bool):
        """Set whether to apply styling based on progress value.

        When enabled, the notification appearance may change based on
        the current progress value (e.g., different colors for different ranges).

        Args:
            styled_by_progress: True to enable progress-based styling, False otherwise.

        Returns:
            ProgressStyle: This ProgressStyle instance for method chaining.
        """
        self.style.setStyledByProgress(styled_by_progress)
        return self

    def get_style(self):
        """Build the ProgressStyle notification style.

        Returns:
            Notification.ProgressStyle: The constructed progress style.

        API Level: Requires API 36+
        """
        return self.style
