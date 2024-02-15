from jnius import PythonJavaClass, java_method


class OnAudioFocusChangeListener(PythonJavaClass):
    __javainterfaces__ = ["android/media/AudioManager$OnAudioFocusChangeListener"]
    __javacontext__ = "app"

    def __init__(self, callback, **kwargs):
        super(OnAudioFocusChangeListener, self).__init__(**kwargs)
        self.callback = callback

    @java_method("(I)V")
    def onAudioFocusChange(self, focus_change):
        self.callback(focus_change)
