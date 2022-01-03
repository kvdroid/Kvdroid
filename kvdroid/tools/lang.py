from kvdroid.jclass.java.util import Locale


def device_lang():
    return Locale().getDefault().getLanguage()
