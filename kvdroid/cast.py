from jnius import cast

# experimental(castables not yet complete, still in hunt)
castable_packages = {
    "parcelable": "android.os.Parcelable",
    "activity": "android.app.Activity",
    "context": "android.content.Context",
    "downloadManager": "android.app.DownloadManager",
    "charSequence": "java.lang.CharSequence",
    "bitmapdrawable": "android.graphics.drawable.BitmapDrawable",
    "adaptiveicondrawable": "android.graphics.drawable.AdaptiveIconDrawable",
    "audioManager": "android.media.AudioManager",
    "uri": "android.net.Uri"
}


def cast_object(name: str, java_object: object):
    if name not in castable_packages:
        raise NameError("Java package name not in predefined castables")
    return cast(castable_packages[name], java_object)
