from kvdroid.jclass.java.util import Locale


def device_lang():
    return Locale().getDefault().getLanguage()


device_lang = device_lang()
