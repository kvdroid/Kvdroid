from kvdroid import Environment


def sdcard():
    return Environment.getExternalStorageDirectory().toString()
sdcard = sdcard()
