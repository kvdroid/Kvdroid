from threading import Semaphore
from kvdroid.jclass.androidx import ExoPlayerBuilder, MediaItem
from kvdroid import activity
from android.runnable import run_on_ui_thread  # NOQA
from kvdroid.util import garbage_collect
from kvdroid.jinterface.media3 import PlayerListener


class ExoPlayer:
    """
    Represents a wrapper for the ExoPlayer that simplifies playback functionalities and
    manages interactions through a listener mechanism.

    This class provides an interface to control media playback using the ExoPlayer framework.
    It supports configuring media items, playback states, repeat modes, and shuffle modes.
    The class handles threading-related complexities through synchronization mechanisms
    and ensures that all ExoPlayer interactions are safely executed on the UI thread.
    It includes various methods for playback control, media item management, and navigation
    within the playlist.

    Attributes:
        COMMAND_GET_CURRENT_MEDIA_ITEM (int): Identifier for the command to get the current media item.
        COMMAND_PLAY_PAUSE (int): Identifier for the play/pause command.
        COMMAND_PREPARE (int): Identifier for the prepare command.
        STATE_BUFFERING (int): Playback state when the player is buffering.
        STATE_ENDED (int): Playback state when the playback has ended.
        STATE_IDLE (int): Playback state when the player is idle.
        STATE_READY (int): Playback state when the player is ready to play.
        REPEAT_MODE_OFF (int): Repeat mode off.
        REPEAT_MODE_ONE (int): Repeat the current media item.
        REPEAT_MODE_ALL (int): Repeat all media items.

    Methods:
        __init__(self): Initializes the ExoPlayer instance and sets up a listener.
        add_listener(self, listener): Adds a listener for player events.
        media_item_from_uri(cls, uri): Creates a media item from a given URI.
        media_item_from_file(cls, file): Creates a media item from a file path.
        set_media_item(self, media_item): Sets a single media item for playback.
        set_media_items(self, media_items): Sets multiple media items for playback.
        set_shuffle_mode_enabled(self, shuffle_mode_enabled): Enables or disables shuffle mode.
        set_repeat_mode(self, repeat_mode): Configures the repeat mode.
        set_media_items_reset_position(self, media_items, reset_position): Sets media items
            and optionally resets the position.
        set_media_items_start_index_start_position(self, media_items, start_index,
            start_position_ms): Sets media items with a specified start index and position.
        add_media_item(self, media_item): Adds a media item to the current media queue.
        clear_media_items(self): Clears all media items from the player.
        prepare(self): Prepares the player for playback.
        play(self): Starts playback.
        pause(self): Pauses playback.
        is_command_available(self, command): Checks if a given command is available.
        is_playing(self): Checks whether the player is currently playing media.
        get_current_position(self): Retrieves the current playback position in milliseconds.
        get_duration(self): Retrieves the total duration of the currently loaded media in milliseconds.
        get_current_media_item_index(self): Retrieves the index of the currently playing media item.
        get_next_media_item_index(self): Retrieves the index of the next media item in the playlist.
        get_previous_media_item_index(self): Retrieves the index of the previous media item in the playlist.
        get_playback_state(self): Retrieves the current state of playback.
        seek_to(self, position_ms): Seeks to a specific position in the current media.
        seek_to_media_item_index(self, media_item_index, position_ms): Seeks to a position
            in a specific media item.
        seek_to_default_position(self, media_item_index): Seeks to the default position of a media item.
        seek_to_next(self): Seeks to the next position in the current media.
        seek_to_next_media_item(self): Seeks to the next media item in the playlist.
        seek_to_previous(self): Seeks to the previous position in the current media.
        seek_to_previous_media_item(self): Seeks to the previous media item in the playlist.
    """
    COMMAND_GET_CURRENT_MEDIA_ITEM = 16
    COMMAND_PLAY_PAUSE = 1
    COMMAND_PREPARE = 2
    STATE_BUFFERING = 2
    STATE_ENDED = 4
    STATE_IDLE = 1
    STATE_READY = 3
    REPEAT_MODE_OFF = 0
    REPEAT_MODE_ONE = 1
    REPEAT_MODE_ALL = 2

    def __init__(self):
        """
        ExoPlayerWrapper is responsible for building and managing an ExoPlayer instance.
        It initializes the player and sets up a custom listener for handling playback
        events and state changes.

        Attributes:
            exoplayer: Instance of the ExoPlayer created through ExoPlayerBuilder.
            _listener: Instance of PlayerListener associated with the player, used
                to handle specific player events.
        """
        self.exoplayer = ExoPlayerBuilder(activity).build()
        self._listener = PlayerListener(self)
        self.add_listener(self._listener)

    def add_listener(self, listener):
        """
        Adds a listener to the ExoPlayer instance and ensures the process runs
        on the UI thread. Utilizes a semaphore to handle concurrent operations.

        Parameters:
            listener: The listener object to be added to the ExoPlayer.

        Returns:
            None
        """
        @run_on_ui_thread
        def add_listener():
            self.exoplayer.addListener(listener)
            garbage_collect()
            lock.release()

        lock = Semaphore(0)
        add_listener()
        lock.acquire()

    @classmethod
    def media_item_from_uri(cls, uri):
        """
            This class method creates a MediaItem instance from the provided URI.

            It utilizes the fromUri method of the MediaItem class to initialize
            and return a new MediaItem object. The purpose of this method is to
            provide a streamlined way to create MediaItem objects using a URI.

            Parameters:
            uri: str
                The URI string used to initialize a MediaItem instance.

            Returns:
            MediaItem
                A new instance of MediaItem initialized using the given URI.

            Raises:
            None
        """
        return MediaItem().fromUri(uri)

    @classmethod
    def media_item_from_file(cls, file: str):
        """
            Creates a MediaItem instance from a file.

            This class method is used to create a MediaItem object by reading and
            initializing it from the specified file.

            Args:
                file: The path to the file from which the MediaItem will be created.

            Returns:
                The MediaItem object initialized using the provided file.
        """
        return MediaItem().fromFile(file)

    def set_media_item(self, media_item):
        """
        Sets the provided media item to the ExoPlayer instance and ensures thread synchronization
        using a Semaphore. The method is also marked to run on the UI thread for compatibility
        with Android GUI operations.

        Args:
            media_item: The media item to be set in the ExoPlayer instance. This should be
            compatible with the requirements of the ExoPlayer's setMediaItem method.
        """
        @run_on_ui_thread
        def set_media_item():
            self.exoplayer.setMediaItem(media_item)
            garbage_collect()
            lock.release()

        lock = Semaphore(0)
        set_media_item()
        lock.acquire()

    def set_media_items(self, media_items):
        """
        Sets the media items for playback on the ExoPlayer instance.

        The method updates the media items to be played by the ExoPlayer. It uses a semaphore lock to
        ensure synchronization when setting the media items. This function must be run on the UI
        thread to ensure thread safety due to interaction with the ExoPlayer framework.

        Args:
            media_items (List[MediaItem]): The list of MediaItem objects to set for playback.

        Returns:
            None
        """
        @run_on_ui_thread
        def set_media_items():
            self.exoplayer.setMediaItems(media_items)
            garbage_collect()
            lock.release()

        lock = Semaphore(0)
        set_media_items()
        lock.acquire()

    def set_shuffle_mode_enabled(self, shuffle_mode_enabled: bool):
        """
        Sets the shuffle mode for the ExoPlayer.

        Shuffle mode determines whether the media items are played in a sequential
        order or shuffled randomly. This method runs on the UI thread and deals with
        thread synchronization through a semaphore lock to ensure proper execution.

        Parameters:
        shuffle_mode_enabled (bool): If True, shuffle mode will be enabled, causing
            media items to be played in a random order. If False, items will be
            played sequentially.
        """
        @run_on_ui_thread
        def set_shuffle_mode_enabled():
            self.exoplayer.setShuffleModeEnabled(shuffle_mode_enabled)
            garbage_collect()
            lock.release()

        lock = Semaphore(0)
        set_shuffle_mode_enabled()
        lock.acquire()

    def set_repeat_mode(self, repeat_mode: int):
        """
        Sets the repeat mode for the media player.

        The repeat mode determines how the media playback should behave when the end of
        the media is reached. It allows controlling whether the media should restart,
        stop, or other possible repeat behaviors.

        Parameters:
            repeat_mode: int
                The desired repeat mode to be set. The specific integer values and their
                corresponding behaviors depend on the configuration and implementation
                details of the exoplayer instance.
        """
        @run_on_ui_thread
        def set_repeat_mode():
            self.exoplayer.setRepeatMode(repeat_mode)
            garbage_collect()
            lock.release()

        lock = Semaphore(0)
        set_repeat_mode()
        lock.acquire()

    def set_media_items_reset_position(self, media_items, reset_position: bool):
        """
        Sets media items and optionally resets the playback position.

        This method updates the list of media items in the ExoPlayer instance,
        allowing for changes to the media queue. It provides an option to reset
        the playback position when the media items are updated.

        Parameters:
        media_items (Any): The media items to be set in the ExoPlayer instance.
        reset_position (bool): A flag indicating whether the playback position
            should be reset when updating media items.
        """
        @run_on_ui_thread
        def set_media_items_reset_position():
            self.exoplayer.setMediaItems(media_items, reset_position)
            garbage_collect()
            lock.release()

        lock = Semaphore(0)
        set_media_items_reset_position()
        lock.acquire()

    def set_media_items_start_index_start_position(self, media_items, start_index: int, start_position_ms: int):
        """
        Sets the media items, playback start index, and playback start position
        in milliseconds for the ExoPlayer instance in the UI thread.

        This method ensures that media items are updated and playback is
        initiated at the specified index and position on ExoPlayer with thread
        synchronization using a Semaphore to block execution until the operation
        is completed.

        Parameters:
            media_items: List[Dict]
                The media items to set. This typically contains a list of
                dictionaries representing the media sources.
            start_index: int
                The index of the first item to play from the media items list.
            start_position_ms: int
                The playback start position in milliseconds for the item at the
                specified start index.
        """
        @run_on_ui_thread
        def set_media_items_start_index_start_position():
            self.exoplayer.setMediaItems(media_items, start_index, start_position_ms)
            garbage_collect()
            lock.release()

        lock = Semaphore(0)
        set_media_items_start_index_start_position()
        lock.acquire()

    def add_media_item(self, media_item):
        """
        Adds a media item to the ExoPlayer instance. This method ensures that
        the media item is added on the user interface thread to maintain thread
        safety. A semaphore is used to synchronize the function execution and
        control the flow until the operation is completed.

        Parameters:
        media_item
            The media item to be added to the ExoPlayer instance.
        """
        @run_on_ui_thread
        def add_media_item():
            self.exoplayer.addMediaItem(media_item)
            garbage_collect()
            lock.release()

        lock = Semaphore(0)
        add_media_item()
        lock.acquire()

    def clear_media_items(self):
        """
        Clears all media items from the ExoPlayer instance.

        This method clears the media playlist of the associated ExoPlayer instance
        and releases the lock to allow further operations. It runs on the UI thread
        to ensure thread safety while interacting with the ExoPlayer.

        Raises:
            None
        """
        @run_on_ui_thread
        def clear_media_items():
            self.exoplayer.clearMediaItems()
            garbage_collect()
            lock.release()

        lock = Semaphore(0)
        clear_media_items()
        lock.acquire()

    def prepare(self):
        """
        Prepares the ExoPlayer instance for playback and synchronizes threading
        using a Semaphore.

        The method ensures that the ExoPlayer instance is prepared on the UI
        thread and coordinates the threading using a Semaphore to provide a
        safe mechanism for thread synchronization.

        Threads will wait on the Semaphore until the preparation process is
        completed.

        Raises:
            This function does not raise exceptions directly. Any raised errors
            should be handled elsewhere.
        """
        @run_on_ui_thread
        def prepare():
            self.exoplayer.prepare()
            garbage_collect()
            lock.release()

        lock = Semaphore(0)
        prepare()
        lock.acquire()

    def play(self):
        """
        This function plays the media using the ExoPlayer instance. It ensures the playback operation
        is executed on the UI thread and uses a semaphore to synchronize operations.

        Parameters:
            None

        Raises:
            None

        Returns:
            None
        """
        @run_on_ui_thread
        def play():
            self.exoplayer.play()
            garbage_collect()
            lock.release()

        lock = Semaphore(0)
        play()
        lock.acquire()

    def pause(self):
        """
            Pauses the playback of the ExoPlayer and releases the lock.

            This function executes on the UI thread as decorated by the @run_on_ui_thread
            decorator. It pauses the ExoPlayer instance by calling its internal `pause` method
            and then releases the lock to unblock the synchronized operation.

            Raises:
                RuntimeError: If called without the corresponding lock being acquired.

            Note:
                Ensure the lock is properly initialized and acquired before calling this
                function to avoid undefined behavior.
        """
        @run_on_ui_thread
        def pause():
            self.exoplayer.pause()
            garbage_collect()
            lock.release()

        lock = Semaphore(0)
        pause()
        lock.acquire()

    def is_command_available(self, command):
        """
        Checks if a specific command is available for execution.

        This function determines the availability of a command by using the exoplayer's
        `isCommandAvailable` method. The function executes on the UI thread and synchronizes
        its operation using a semaphore to ensure the availability check is completed before
        returning the result.

        Parameters:
        command : Any
            The command to check for availability.

        Returns:
        bool
            True if the specified command is available, otherwise False.
        """
        @run_on_ui_thread
        def is_command_available():
            nonlocal available
            available = self.exoplayer.isCommandAvailable(command)
            garbage_collect()
            lock.release()

        available = False
        lock = Semaphore(0)
        is_command_available()
        lock.acquire()
        return available

    def is_playing(self):
        """
        Checks if the player is currently playing.

        This function is executed on the UI thread and determines whether the
        player is in a playing state by querying the exoplayer instance. It
        utilizes a semaphore to synchronize the completion of the operation.

        Returns
        -------
        bool
            True if the player is currently playing, False otherwise.
        """
        @run_on_ui_thread
        def is_playing():
            nonlocal playing
            playing = self.exoplayer.isPlaying()
            garbage_collect()
            lock.release()

        playing = False
        lock = Semaphore(0)
        is_playing()
        lock.acquire()
        return playing

    def get_current_position(self):
        """
        Fetches the current playback position of the ExoPlayer in milliseconds.

        This method retrieves the position in the media track the ExoPlayer
        is currently at. It ensures thread safety for UI operations and utilizes
        a semaphore to synchronize the completion of fetching this value.

        Returns:
            int: The current playback position in milliseconds as retrieved
            from the ExoPlayer.
        """
        @run_on_ui_thread
        def get_current_position():
            nonlocal position
            position = self.exoplayer.getCurrentPosition()
            garbage_collect()
            lock.release()

        position = 0
        lock = Semaphore(0)
        get_current_position()
        lock.acquire()
        return position

    def get_duration(self):
        """
        Retrieves the duration of the media being played using the ExoPlayer instance
        and returns the value. This is a blocking call that waits for the duration to
        be retrieved and is executed on the UI thread.

        Returns:
            int: The duration of the media in milliseconds.
        """
        @run_on_ui_thread
        def get_duration():
            nonlocal duration
            duration = self.exoplayer.getDuration()
            garbage_collect()
            lock.release()

        duration = 0
        lock = Semaphore(0)
        get_duration()
        lock.acquire()
        return duration

    def get_current_media_item_index(self):
        """
        Retrieve the index of the currently playing media item.

        This function fetches the currently playing media item index from the
        ExoPlayer instance. It is designed to ensure thread safety by using a
        semaphore to synchronize execution and return the result correctly.

        Arguments:
            None

        Raises:
            None

        Returns:
            int: The index of the currently playing media item.
        """
        @run_on_ui_thread
        def get_current_media_item_index():
            nonlocal index
            index = self.exoplayer.getCurrentMediaItemIndex()
            garbage_collect()
            lock.release()

        index = -1
        lock = Semaphore(0)
        get_current_media_item_index()
        lock.acquire()
        return index

    def get_next_media_item_index(self):
        """
        Gets the index of the next media item in the playback queue.

        This function is executed on the UI thread to ensure thread safety with
        other operations on the ExoPlayer instance. It manages synchronization
        using a semaphore to ensure the index value is set before the function
        returns.

        Returns:
            int: The index of the next media item in the playback queue.
        """
        @run_on_ui_thread
        def get_next_media_item_index():
            nonlocal index
            index = self.exoplayer.getNextMediaItemIndex()
            garbage_collect()
            lock.release()

        index = -1
        lock = Semaphore(0)
        get_next_media_item_index()
        lock.acquire()
        return index

    def get_previous_media_item_index(self):
        """
        Gets the index of the previous media item being played on the ExoPlayer.
        The method fetches the index on the main UI thread to ensure thread safety,
        and uses a semaphore to wait for the asynchronous operation to complete.

        Parameters
        ----------
        No parameters.

        Returns
        -------
        int
            The index of the previous media item or -1 if no previous media item
            exists.
        """
        @run_on_ui_thread
        def get_previous_media_item_index():
            nonlocal index
            index = self.exoplayer.getPreviousMediaItemIndex()
            garbage_collect()
            lock.release()

        index = -1
        lock = Semaphore(0)
        get_previous_media_item_index()
        lock.acquire()
        return index

    def get_playback_state(self):
        """
        Gets the current playback state of the ExoPlayer instance on the UI thread.

        This function interacts with an ExoPlayer instance to retrieve its current
        playback state while ensuring thread safety with the use of a semaphore.

        Returns
        -------
        int
            The playback state of the ExoPlayer instance. Possible states include:
            - `STATE_IDLE`: The ExoPlayer instance is idle and not ready to play.
            - `STATE_BUFFERING`: The ExoPlayer instance is buffering content.
            - `STATE_READY`: The ExoPlayer instance is ready to play.
            - `STATE_ENDED`: The ExoPlayer instance has finished playing.
        """
        @run_on_ui_thread
        def get_playback_state():
            nonlocal state
            state = self.exoplayer.getPlaybackState()
            garbage_collect()
            lock.release()

        state = self.STATE_IDLE
        lock = Semaphore(0)
        get_playback_state()
        lock.acquire()
        return state

    def seek_to(self, position_ms: int):
        """
        Adjusts the playback position to a specified time in milliseconds.

        This method updates the media playback position to the specified
        value, allowing precise control over playback. It ensures thread-safe
        interactions with the underlying media player by using a semaphore to
        synchronize the operation.

        Args:
            position_ms (int): The desired playback position in milliseconds.
        """
        @run_on_ui_thread
        def seek_to():
            self.exoplayer.seekTo(position_ms)
            garbage_collect()
            lock.release()

        lock = Semaphore(0)
        seek_to()
        lock.acquire()

    def seek_to_media_item_index(self, media_item_index: int, position_ms: int = 0):
        """
        Seek to a specified media item index with an optional position offset.

        This function allows seeking to a specific media item within a playlist
        using the provided index. Additionally, an offset position in milliseconds
        can be provided to start playback from a precise timestamp within the media
        item. The method ensures thread safety by making use of a semaphore lock.

        Parameters:
            media_item_index (int): Index of the media item to seek to within the
                playlist.
            position_ms (int, optional): Position in milliseconds to seek to within
                the specified media item. Defaults to 0.
        """
        @run_on_ui_thread
        def seek_to():
            self.exoplayer.seekTo(media_item_index, position_ms)
            garbage_collect()
            lock.release()

        lock = Semaphore(0)
        seek_to()
        lock.acquire()

    def seek_to_default_position(self, media_item_index: int = None):
        """
        Seek to the default position of the current media item or to the default position of the specified media item.

        Parameters:
        media_item_index (int, optional): The index of the media item to seek to its
        default position. If not provided, seeks to the default position of the current
        media item.
        """
        @run_on_ui_thread
        def seek_to_default_position():
            if media_item_index is not None:
                self.exoplayer.seekToDefaultPosition(media_item_index)
            else:
                self.exoplayer.seekToDefaultPosition()
            garbage_collect()
            lock.release()

        lock = Semaphore(0)
        seek_to_default_position()
        lock.acquire()

    def seek_to_next(self):
        """
        Implements a method to seek to the next track in a media player and ensures the
        method is executed on the UI thread. The operation releases a semaphore lock
        upon completion.

        lock : Semaphore
            A semaphore instance to synchronize the method execution by ensuring the
            method waits until the seeking operation is complete.

        Methods
        -------
        seek_to_next():
            Seeks to the next media track in the ExoPlayer instance and releases the
            semaphore lock upon completion.
        """
        @run_on_ui_thread
        def seek_to_next():
            self.exoplayer.seekToNext()
            garbage_collect()
            lock.release()

        lock = Semaphore(0)
        seek_to_next()
        lock.acquire()

    def seek_to_next_media_item(self):
        """
        This function seeks to the next media item in the playback queue using the
        ExoPlayer instance. It ensures the operation is performed on the UI thread,
        providing thread safety for UI-related actions. After invoking the seek
        operation, a semaphore is released to signal completion.

        Attributes:
            lock (Semaphore): A semaphore used to synchronize the execution flow,
            ensuring the seek operation completes before continuing.

        Raises:
            AttributeError: If `self.exoplayer` or `self.exoplayer.seekToNextMediaItem`
            is not properly defined.
        """
        @run_on_ui_thread
        def seek_to_next_media_item():
            self.exoplayer.seekToNextMediaItem()
            garbage_collect()
            lock.release()

        lock = Semaphore(0)
        seek_to_next_media_item()
        lock.acquire()

    def seek_to_previous(self):
        """
        Acquires a lock, seeks the ExoPlayer to the previous media item, and then releases the lock.

        This function is designed to be run on the UI thread, interfacing with the ExoPlayer instance
        to move to the previous item in the playlist. A semaphore lock ensures the operation completes
        synchronously.

        Raises
        ------
            No specific exceptions are raised directly by this function; however, improper handling of
            locks or UI thread operations may lead to side effects or unexpected behavior.
        """
        @run_on_ui_thread
        def seek_to_previous():
            self.exoplayer.seekToPrevious()
            garbage_collect()
            lock.release()

        lock = Semaphore(0)
        seek_to_previous()
        lock.acquire()

    def seek_to_previous_media_item(self):
        """
        Seek to the previous media item in the playback queue.

        This function is used to navigate to the previous media
        item using the internal ExoPlayer instance. The function
        ensures execution on the UI thread.

        Args: None

        Returns: None
        """
        @run_on_ui_thread
        def seek_to_previous_media_item():
            self.exoplayer.seekToPreviousMediaItem()
            garbage_collect()
            lock.release()

        lock = Semaphore(0)
        seek_to_previous_media_item()
        lock.acquire()

    def on_position_discontinuity(self, old_position, new_position, reason: int):
        pass

    def on_events(self, player, events):
        pass

    def on_timeline_changed(self, timeline, reason: int):
        pass

    def on_media_item_transition(self, media_item, reason: int):
        pass

    def on_tracks_changed(self, tracks_info):
        pass

    def on_media_metadata_changed(self, media_metadata):
        pass

    def on_playlist_metadata_changed(self, playlist_metadata):
        pass

    def on_is_loading_changed(self, is_loading: bool):
        pass

    def on_loading_changed(self, is_loading: bool):
        pass

    def on_available_commands_changed(self, commands):
        pass

    def on_track_selection_parameters_changed(self, parameters):
        pass

    def on_player_state_changed(self, play_when_ready: bool, playback_state: int):
        pass

    def on_playback_state_changed(self, playback_state: int):
        pass

    def on_play_when_ready_changed(self, play_when_ready: bool, reason: int):
        pass

    def on_playback_suppression_reason_changed(self, suppression_reason: int):
        pass

    def on_is_playing_changed(self, is_playing: bool):
        pass

    def on_repeat_mode_changed(self, repeat_mode: int):
        pass

    def on_shuffle_mode_enabled_changed(self, shuffle_mode_enabled: bool):
        pass

    def on_player_error(self, error):
        pass

    def on_player_error_changed(self, error):
        pass

    def on_playback_parameters_changed(self, playback_parameters):
        pass

    def on_seek_back_increment_changed(self, seek_back_increment_ms: int):
        pass

    def on_seek_forward_increment_changed(self, seek_forward_increment_ms: int):
        pass

    def on_max_seek_to_previous_position_changed(self, max_seek_to_previous_position_ms: int):
        pass

    def on_audio_session_id_changed(self, audio_session_id: int):
        pass

    def on_audio_attributes_changed(self, audio_attributes):
        pass

    def on_volume_changed(self, volume: float):
        pass

    def on_skip_silence_enabled_changed(self, skip_silence_enabled: bool):
        pass

    def on_device_info_changed(self, device_info):
        pass

    def on_device_volume_changed(self, volume: int, muted: bool):
        pass

    def on_video_size_changed(self, video_size):
        pass

    def on_surface_size_changed(self, width: int, height: int):
        pass

    def on_rendered_first_frame(self, rendered_surface):
        pass

    def on_cues(self, cues):
        pass

    def on_cues_group(self, cue_group):
        pass

    def on_metadata(self, metadata):
        pass
