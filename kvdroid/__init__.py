from kivy.utils import platform
from kivy.logger import Logger

if platform == "android":
    try:
        from kivy.core.window import Window
        from jnius import autoclass,cast
        from android.runnable import run_on_ui_thread 
        
        AndroidActivity = autoclass('android.app.Activity')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity        
        Build = autoclass("android.os.Build")
        VERSION = autoclass('android.os.Build$VERSION')
        VERSION_CODES = autoclass("android.os.Build$VERSION_CODES")        
        View = autoclass('android.view.View')        
        Color = autoclass("android.graphics.Color")
        WindowManager = autoclass('android.view.WindowManager$LayoutParams')
        Intent = autoclass('android.content.Intent')
        Provider = autoclass('android.provider.Settings')
        Uri = autoclass('android.net.Uri')
        Locale = autoclass('java.util.Locale')
        ConnectivityManager = autoclass('android.net.ConnectivityManager')
        Configuration = autoclass("android.content.res.Configuration")
        Environment = autoclass("android.os.Environment")
        File = autoclass('java.io.File')
        BitmapFactory = autoclass('android.graphics.BitmapFactory')
        WallpaperManager = autoclass('android.app.WallpaperManager')
        TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
        Context = autoclass('android.content.Context')
        Request = autoclass("android.app.DownloadManager$Request")
        Runtime = autoclass('java.lang.Runtime')
        String = autoclass("java.lang.String")
        StrictMode = autoclass('android.os.StrictMode')
        MediaPlayer = autoclass('android.media.MediaPlayer')
        AudioManager = autoclass('android.media.AudioManager')
        
    except BaseException:
        Logger.error(
            "Kvdroid: Cannot load classes by Pyjnius. Make sure requirements installed"
        )
else:
    Logger.error(
        "Kvdroid: Kvdroid is only callable for Android"
    )
