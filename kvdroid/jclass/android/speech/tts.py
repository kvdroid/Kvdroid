from jnius import autoclass
from kvdroid.jclass import _class_call


def TextToSpeech(*args, instantiate: bool = False):
    return _class_call(autoclass('android.speech.tts.TextToSpeech'), args, instantiate)
