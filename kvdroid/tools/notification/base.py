__all__ = ("Builder", "Person")

from abc import ABC, abstractmethod

from kvdroid.jclass.androidx import PersonBuilder, IconCompat
from kvdroid.tools.graphics import get_bitmap


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
        icon = IconCompat().createWithBitmap(bitmap)
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
