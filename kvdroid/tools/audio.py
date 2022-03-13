from threading import Thread
from typing import Callable
from jnius.jnius import JavaException
from kvdroid.jclass.android import MediaPlayer, AudioManager


class Player(object):
    mPlayer = MediaPlayer(instantiate=True)
    content = None

    def raw(self):
        return self.mPlayer

    def play(self, content: str):
        self.content = content
        try:
            self.mPlayer.stop()
            self.mPlayer.reset()
        except JavaException:
            pass
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
        try:
            from kivy.clock import mainthread # NOQA
            @mainthread # NOQA
            def load_finish():
                on_load_finish()
        except ImportError:
            from android.runnable import run_on_ui_thread  # NOQA
            @run_on_ui_thread # NOQA
            def load_finish():
                on_load_finish()
        self.content = content
        self.mPlayer.setAudioStreamType(AudioManager().STREAM_MUSIC)
        try:
            self.mPlayer.stop()
            self.mPlayer.reset()
        except JavaException:
            pass
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
