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
        except:
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

    def stream(self, content: str):
        self.content = content
        self.mPlayer.setAudioStreamType(AudioManager().STREAM_MUSIC)
        try:
            self.mPlayer.stop()
            self.mPlayer.reset()
        except:
            pass
        self.mPlayer.setDataSource(self.content)
        self.mPlayer.prepare()
        self.mPlayer.start()

    def get_duration(self):
        if self.content:
            return self.mPlayer.getDuration()

    def current_position(self):
        if self.content:
            return self.mPlayer.getCurrentPosition()

    def seek(self, value: int):
        try:
            self.mPlayer.seekTo(value * 1000)
        except:
            pass

    def do_loop(self, loop=False):
        if not loop:
            self.mPlayer.setLooping(False)
        else:
            self.mPlayer.setLooping(True)

    def is_playing(self):
        return self.mPlayer.isPlaying()
