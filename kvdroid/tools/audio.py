from threading import Thread
from typing import Callable
from jnius import JavaException
from kvdroid.jinterface.media import OnAudioFocusChangeListener

from kvdroid.jclass.android import (
    MediaPlayer, AudioManager,
    MediaStoreAudioMedia, ContentUris,
    MediaStoreAudioCoulmns, MediaStoreMediaColumns,
    Size, Context, VERSION, MediaStoreAudioAlbumColumns
)
from kvdroid.cast import cast_object
from kvdroid import activity


class Player:
    def __init__(self, on_audio_focus_change: Callable = None):
        self.on_audio_focus_change = on_audio_focus_change
        self.mPlayer = None
        self.content = None

    def raw(self):
        return self.mPlayer

    def play(self, content: str):
        if not self.mPlayer:
            self.mPlayer = MediaPlayer(instantiate=True)
        self.content = content
        self.mPlayer.stop()
        self.mPlayer.reset()
        self.mPlayer.setDataSource(self.content)
        self.mPlayer.prepare()
        self.mPlayer.start()

    def pause(self):
        self.mPlayer.pause()

    def resume(self):
        self.mPlayer.start()

    def stop(self):
        self.mPlayer.stop()

    def stream(self, content: str, on_load_finish: Callable = lambda: None):
        Thread(target=self._stream, args=(content, on_load_finish)).start()

    def _stream(self, content: str, on_load_finish: Callable):
        if not self.mPlayer:
            self.mPlayer = MediaPlayer(instantiate=True)
        try:
            from kivy.clock import mainthread  # NOQA
            @mainthread  # NOQA
            def load_finish():
                on_load_finish()
        except ImportError:
            from android.runnable import run_on_ui_thread  # NOQA
            @run_on_ui_thread  # NOQA
            def load_finish():
                on_load_finish()
        self.content = content
        self.mPlayer.setAudioStreamType(AudioManager().STREAM_MUSIC)
        self.mPlayer.stop()
        self.mPlayer.reset()
        self.mPlayer.setDataSource(self.content)
        self.mPlayer.prepare()
        self.mPlayer.start()
        load_finish()

    def get_duration(self):
        if self.content:
            return self.mPlayer.getDuration()

    def current_position(self):
        if self.content:
            return self.mPlayer.getCurrentPosition()

    def seek(self, value: int):
        try:
            self.mPlayer.seekTo(value * 1000)
        except JavaException:
            pass

    def do_loop(self, loop=False):
        if not loop:
            self.mPlayer.setLooping(False)
        else:
            self.mPlayer.setLooping(True)

    def is_playing(self):
        return self.mPlayer.isPlaying()

    def release_media_player(self):
        if not self.mPlayer:
            return
        self.mPlayer.release()
        self.mPlayer = None

    def _on_audio_focus_change(self, focus_change):
        if focus_change == AudioManager().AUDIOFOCUS_LOSS:
            self.stop()
        elif focus_change == AudioManager().AUDIOFOCUS_LOSS_TRANSIENT:
            self.pause()
        elif focus_change == AudioManager().AUDIOFOCUS_LOSS_TRANSIENT_CAN_DUCK:
            self.mPlayer.setVolume(0.2, 0.2)
        elif focus_change == AudioManager().AUDIOFOCUS_GAIN:
            self.mPlayer.setVolume(1.0, 1.0)
            self.resume()

    def user_defined_focus_change(self, focus_change):
        if focus_change == AudioManager().AUDIOFOCUS_LOSS:
            self.on_audio_focus_change("AUDIOFOCUS_LOSS")
        elif focus_change == AudioManager().AUDIOFOCUS_LOSS_TRANSIENT:
            self.on_audio_focus_change("AUDIOFOCUS_LOSS_TRANSIENT")
        elif focus_change == AudioManager().AUDIOFOCUS_LOSS_TRANSIENT_CAN_DUCK:
            self.on_audio_focus_change("AUDIOFOCUS_LOSS_TRANSIENT_CAN_DUCK")
        elif focus_change == AudioManager().AUDIOFOCUS_GAIN:
            self.on_audio_focus_change("AUDIOFOCUS_GAIN")

    def request_audio_focus(self):
        focusChangeListener = OnAudioFocusChangeListener(
            callback=self.user_defined_focus_change or self._on_audio_focus_change)
        am = cast_object("audioManager", activity.getSystemService(Context().AUDIO_SERVICE))
        result = am.requestAudioFocus(focusChangeListener, AudioManager().STREAM_MUSIC, AudioManager().AUDIOFOCUS_GAIN)
        if result == AudioManager().AUDIOFOCUS_REQUEST_GRANTED:
            return True
        return False


def get_all_audio_files(
        content_resolver=None,
        projection=None,
        selection=None,
        selection_args=None,
        sort_order=None,
        thumbnail_size=None
):
    """
    Retrieves all audio files from the device's media store. This function queries the media store
    for audio files and yields each file's metadata, including its ID, display name, data location,
    title, duration, size, album, artist, URI, and thumbnail. It supports querying with customizable
    parameters such as projection, selection, selection arguments, sort order, and thumbnail size.

    The function utilizes the device's `ContentResolver` to query the media store database and fetch
    the desired audio file information. If not provided, default queries are used to select only
    valid music files with `.mp3` extensions. Additionally, it provides compatibility for SDK versions
    both above and below 29 for handling thumbnails.

    :param content_resolver: The content resolver instance used to query the device's media store.
        If not provided, the default application's content resolver is used.
    :type content_resolver: android.content.ContentResolver, optional
    :param projection: List of media columns to be retrieved. If not provided, a default set of columns
        such as ID, display name, data, title, etc., will be queried.
    :type projection: list of str, optional
    :param selection: SQL WHERE clause to filter the audio files. By default, it filters music files
        with non-empty titles and display names ending with '.mp3'.
    :type selection: str, optional
    :param selection_args: Arguments for the SQL WHERE clause. Defaults to a list containing a
        single string `%.mp3`.
    :type selection_args: list of str, optional
    :param sort_order: SQL ORDER BY clause to sort the results. If not provided, files are sorted
        by display name in ascending order.
    :type sort_order: str, optional
    :param thumbnail_size: Size of the thumbnails to be generated. Defaults to a 512x512 pixel size.
    :type thumbnail_size: list of int, optional
    :return: A generator that yields dictionaries representing audio file metadata, including keys
        like `id`, `display_name`, `data`, `title`, `duration`, `size`, `album`, `artist`,
        `uri`, and `thumbnail`.
    :rtype: generator of dict
    """

    Media = MediaStoreAudioMedia()
    AudioColumns = MediaStoreAudioCoulmns()
    MediaColumns = MediaStoreMediaColumns()
    music_uri = Media.EXTERNAL_CONTENT_URI
    if not projection:
        projection = [
            Media._ID,
            MediaColumns.DISPLAY_NAME,
            MediaColumns.DATA,
            MediaColumns.TITLE,
            MediaColumns.DURATION,
            MediaColumns.SIZE,
            AudioColumns.ALBUM,
            AudioColumns.ARTIST,
            AudioColumns.IS_MUSIC,
        ]
    if VERSION().SDK_INT < 29:
        projection.append(MediaStoreAudioAlbumColumns().ALBUM_ART)
    if not content_resolver:
        content_resolver = activity.getApplicationContext().getContentResolver()
    if not selection:
        selection = f"{Media.IS_MUSIC} != 0 AND {Media.TITLE} != '' AND {Media.DISPLAY_NAME} LIKE ?"
    if not selection_args:
        selection_args = ["%.mp3"]
    if not sort_order:
        sort_order = f"{Media.DISPLAY_NAME} ASC"
    if not thumbnail_size:
        thumbnail_size = [512, 512]

    cursor = content_resolver.query(music_uri, projection, selection, selection_args, sort_order)
    id_column = cursor.getColumnIndexOrThrow(Media._ID)
    name_column = cursor.getColumnIndexOrThrow(Media.DISPLAY_NAME)
    data_column = cursor.getColumnIndexOrThrow(Media.DATA)
    title_column = cursor.getColumnIndexOrThrow(Media.TITLE)
    duration_column = cursor.getColumnIndexOrThrow(Media.DURATION)
    size_column = cursor.getColumnIndexOrThrow(Media.SIZE)
    album_column = cursor.getColumnIndexOrThrow(Media.ALBUM)
    artist_column = cursor.getColumnIndexOrThrow(Media.ARTIST)
    if VERSION().SDK_INT < 29:
        thumbnail_column = cursor.getColumnIndexOrThrow(MediaStoreAudioAlbumColumns().ALBUM_ART)
    else:
        thumbnail_column = None

    if cursor:
        try:
            while cursor.moveToNext():
                audio = dict(
                    id=cursor.getLong(id_column),
                    display_name=cursor.getString(name_column),
                    data=cursor.getString(data_column),
                    title=cursor.getString(title_column),
                    duration=cursor.getLong(duration_column),
                    size=cursor.getLong(size_column),
                    album=cursor.getString(album_column),
                    artist=cursor.getString(artist_column),
                )
                audio["uri"] = ContentUris().withAppendedId(music_uri, audio["id"])
                from tinytag import TinyTag
                
                try:
                    if VERSION().SDK_INT >= 29:
                        audio["thumbnail"] = content_resolver.loadThumbnail(audio["uri"], Size(*thumbnail_size), None)
                    else:
                        audio["thumbnail"] = cursor.getString(thumbnail_column)
                except JavaException:
                    audio["thumbnail"] = None
                yield audio
        finally:
            cursor.close()
