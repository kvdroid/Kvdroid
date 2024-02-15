from threading import Thread
from typing import Callable
from jnius import JavaException
from kvdroid.jclass.android import MediaPlayer, AudioManager
from kvdroid.cast import cast_object
from kvdroid import activity
from kvdroid.jclass.android import Context


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
