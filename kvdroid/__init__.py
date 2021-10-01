import logging
import webbrowser
from os import environ
from jnius.jnius import JavaException


def _get_platform():
    # On Android sys.platform returns 'linux2', so prefer to check the
    # existence of environ variables set during Python initialization
    kivy_build = environ.get('KIVY_BUILD', '')
    if kivy_build in {'android', 'ios'}:
        return kivy_build
    elif 'P4A_BOOTSTRAP' in environ:
        return 'android'
    elif 'ANDROID_ARGUMENT' in environ:
        # We used to use this method to detect android platform,
        # leaving it here to be backwards compatible with `pydroid3`
        # and similar tools outside kivy's ecosystem
        return 'android'


platform = _get_platform()
Logger = logging.getLogger('kivy')

if platform == "android":
    try:
        from jnius import autoclass, cast, JavaException
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
        PendingIntent = autoclass("android.app.PendingIntent")
        Provider = autoclass('android.provider.Settings')
        URLConnection = autoclass("java.net.URLConnection")
        Toast = autoclass('android.widget.Toast')
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
        Rect = autoclass('android.graphics.Rect')()
        StatFs = autoclass("android.os.StatFs")
        MemoryInfo = autoclass('android.app.ActivityManager$MemoryInfo')
        BatteryManager = autoclass("android.os.BatteryManager")
        IntentFilter = autoclass("android.content.IntentFilter")
        Point = autoclass("android.graphics.Point")
        CookieManager = autoclass("android.webkit.CookieManager")
        Contacts = autoclass('android.provider.ContactsContract$Contacts')
        Phone = autoclass('android.provider.ContactsContract$CommonDataKinds$Phone')
        ArrayList = autoclass('java.util.ArrayList')
        NotificationManager = autoclass("android.app.NotificationManager")

        if VERSION.SDK_INT >= 26:
            NotificationChannel = autoclass("android.app.NotificationChannel")
            try:
                NotificationManagerCompat = autoclass("androidx.core.app.NotificationManagerCompat")
            except JavaException:
                Logger.error("Kvdroid: Androidx Not Enabled. Skipping....")

        try:
            NotificationCompat = autoclass("androidx.core.app.NotificationCompat")
            NotificationCompatBigPictureStyle = autoclass("androidx.core.app.NotificationCompat$BigPictureStyle")
            NotificationCompatAction = autoclass("androidx.core.app.NotificationCompat$Action")
            NotificationCompatActionBuilder = autoclass("androidx.core.app.NotificationCompat$Action$Builder")
            NotificationCompatBuilder = autoclass("androidx.core.app.NotificationCompat$Builder")
            RemoteInput = autoclass("androidx.core.app.RemoteInput")
            RemoteInputBuilder = autoclass("androidx.core.app.RemoteInput$Builder")
        except JavaException:
            Logger.error("Kvdroid: Androidx Not Enabled. Skipping....")
        NotificationManage = autoclass("android.app.NotificationManager")
        System = autoclass("java.lang.System")

        packages = {
            "whatsapp": "com.whatsapp",
            "facebook": "com.facebook.katana",
            "facebookLite": "com.facebook.lite",
            "oldFacebook": "com.facebook.android",
            "linkedin": "com.linkedin.android",
            "fbMessenger": "com.facebook.orca",
            "fbMessengerLite": "com.facebook.mlite",
            "tiktok": "com.zhiliaoapp.musically",
            "tiktokLite": "com.zhiliaoapp.musically.go",
            "twitter": "com.twitter.android",
            "twitterLite": "com.twitter.android.lite",
            "telegram": "org.telegram.messenger",
            "telegramX": "org.thunderdog.challegram",
            "snapchat": "com.snapchat.android"
        }

    except JavaException:
        Logger.error(
            "Kvdroid: Cannot load classes by Pyjnius. Make sure requirements installed\n"
        )


    def keyboard_height():
        try:
            decor_view = activity.getWindow().getDecorView()
            height = activity.getWindowManager().getDefaultDisplay().getHeight()
            decor_view.getWindowVisibleDisplayFrame(Rect)
            return height - Rect.bottom
        except:
            return 0


    def device_info(text, convert=False):
        bm = activity.getSystemService(Context.BATTERY_SERVICE)
        count = bm.getIntProperty(BatteryManager.BATTERY_PROPERTY_CHARGE_COUNTER)
        cap = bm.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY)
        intent = activity.registerReceiver(None, IntentFilter(Intent.ACTION_BATTERY_CHANGED))

        def convert_bytes(num):
            step_unit = 1000.0  # 1024 bad the size
            for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
                if num < step_unit:
                    return "%3.1f %s" % (num, x)
                num /= step_unit

        def avail_mem():
            stat = StatFs(Environment.getDataDirectory().getPath())
            bytesAvailable = stat.getBlockSize() * stat.getAvailableBlocks()
            if convert:
                return convert_bytes(bytesAvailable)
            else:
                return bytesAvailable

        def total_mem():
            stat = StatFs(Environment.getDataDirectory().getPath())
            bytesAvailable = stat.getBlockSize() * stat.getBlockCount()
            if convert:
                return convert_bytes(bytesAvailable)
            else:
                return bytesAvailable

        def used_mem():
            stat = StatFs(Environment.getDataDirectory().getPath())
            total = stat.getBlockSize() * stat.getBlockCount()
            avail = stat.getBlockSize() * stat.getAvailableBlocks()
            if convert:
                return convert_bytes(total - avail)
            else:
                return total - avail

        def avail_ram():
            memInfo = MemoryInfo()
            service = activity.getSystemService(Context.ACTIVITY_SERVICE)
            service.getMemoryInfo(memInfo)
            if convert:
                return convert_bytes(memInfo.availMem)
            else:
                return memInfo.availMem

        def total_ram():
            memInfo = MemoryInfo()
            service = activity.getSystemService(Context.ACTIVITY_SERVICE)
            service.getMemoryInfo(memInfo)
            if convert:
                return convert_bytes(memInfo.totalMem)
            else:
                return memInfo.totalMem

        def used_ram():
            memInfo = MemoryInfo()
            service = activity.getSystemService(Context.ACTIVITY_SERVICE)
            service.getMemoryInfo(memInfo)
            if convert:
                return convert_bytes(memInfo.totalMem - memInfo.availMem)
            else:
                return memInfo.totalMem - memInfo.availMem

        os = {
            'model': Build.MODEL,
            'brand': Build.BRAND,
            'manufacturer': Build.MANUFACTURER,
            'version': VERSION.RELEASE,
            'sdk': VERSION.SDK,
            'product': Build.PRODUCT,
            'base': VERSION.BASE_OS,
            'rom': VERSION.INCREMENTAL,
            'security': VERSION.SECURITY_PATCH,
            'hardware': Build.HARDWARE,
            'tags': Build.TAGS,
            'sdk_int': VERSION.SDK_INT,
            'cpu_abi': Build.CPU_ABI,
            'cpu_cores': Runtime.getRuntime().availableProcessors(),
            'avail_mem': avail_mem(),
            'total_mem': total_mem(),
            'used_mem': used_mem(),
            'avail_ram': avail_ram(),
            'total_ram': total_ram(),
            'used_ram': used_ram(),
            'bat_level': bm.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY),
            'bat_capacity': round((count / cap) * 100),
            'bat_tempeture': intent.getIntExtra(BatteryManager.EXTRA_TEMPERATURE, 0) / 10,
            'bat_voltage': float(intent.getIntExtra(BatteryManager.EXTRA_VOLTAGE, 0) * 0.001),
            'bat_technology': intent.getStringExtra(BatteryManager.EXTRA_TECHNOLOGY)
        }
        return os[text]


    @run_on_ui_thread
    def immersive_mode(immerse=None):
        if immerse:
            window = activity.getWindow()
            return window.getDecorView().setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                | View.SYSTEM_UI_FLAG_FULLSCREEN
                | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY)


    def launch_app(app_package, app_activity):
        intent = Intent()
        intent.setAction(Intent.ACTION_VIEW)
        intent.setClassName(app_package, app_activity)
        return activity.startActivity(intent)


    def app_details(app_package):
        intent = Intent()
        intent.setAction(Provider.ACTION_APPLICATION_DETAILS_SETTINGS)
        uri = Uri.parse("package:" + app_package)
        intent.setData(uri)
        activity.startActivity(intent)


    @run_on_ui_thread
    def change_statusbar_color(color, text_color, set_nav_color=True):
        window = activity.getWindow()
        if str(text_color) == "black":
            window.getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR)
        elif str(text_color) == "white":
            window.getDecorView().setSystemUiVisibility(0)
        else:
            raise TypeError("Available options are ['white','black'] for StatusBar text color")
        window.clearFlags(WindowManager.FLAG_TRANSLUCENT_STATUS)
        window.addFlags(WindowManager.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
        window.setStatusBarColor(Color.parseColor(str(color)))
        if set_nav_color:
            window.setNavigationBarColor(Color.parseColor(color))


    @run_on_ui_thread
    def navbar_color(color):
        window = activity.getWindow()
        window.setNavigationBarColor(Color.parseColor(str(color)))


    def toast(message):
        return PythonActivity.toastError(str(message))


    def set_wallpaper(path_to_image):
        context = cast('android.content.Context', activity.getApplicationContext())
        file = File(str(path_to_image))
        bitmap = BitmapFactory.decodeFile(file.getAbsolutePath())
        manager = WallpaperManager.getInstance(context)
        return manager.setBitmap(bitmap)


    def speech(text, lang):
        tts = TextToSpeech(activity, None)
        tts.setLanguage(Locale(str(lang)))
        return tts.speak(str(text), TextToSpeech.QUEUE_FLUSH, None)


    def download_manager(title, description, url, folder, file_name):
        uri = Uri.parse(str(url))
        dm = cast("android.app.DownloadManager", activity.getSystemService(Context.DOWNLOAD_SERVICE))
        request = Request(uri)
        request.setTitle(str(title))
        request.setDescription(str(description))
        request.setNotificationVisibility(Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
        request.setDestinationInExternalPublicDir(str(folder), str(file_name))
        dm.enqueue(request)


    def restart_app(restart=False):
        if restart:
            currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
            context = cast('android.content.Context', currentActivity.getApplicationContext())
            packageManager = context.getPackageManager()
            intent = packageManager.getLaunchIntentForPackage(context.getPackageName())
            componentName = intent.getComponent()
            mainIntent = Intent.makeRestartActivityTask(componentName)
            context.startActivity(mainIntent)
            Runtime.getRuntime().exit(0)


    def share_text(text, title='Share', chooser=False, app_package=None, call_playstore=True, error_msg=""):
        intent = Intent()
        intent.setAction(Intent.ACTION_SEND)
        intent.putExtra(Intent.EXTRA_TEXT, String(str(text)))
        intent.setType("text/plain")
        if app_package:
            app_package = packages[app_package] if app_package in packages else None
            try:
                intent.setPackage(String(app_package))
            except JavaException:
                if call_playstore:
                    webbrowser.open(f"http://play.google.com/store/apps/details?id={app_package}")
                toast(error_msg) if error_msg else Logger.error("Kvdroid: Specified Application is unavailable")
                return
        if chooser:
            chooser = Intent.createChooser(intent, String(title))
            activity.startActivity(chooser)
        else:
            activity.startActivity(intent)


    def share_file(path, title='Share', chooser=True, app_package=None, call_playstore=True, error_msg=""):
        path = str(path)
        if VERSION.SDK_INT >= 24:
            StrictMode.disableDeathOnFileUriExposure()
        shareIntent = Intent(Intent.ACTION_SEND)
        shareIntent.setType("*/*")
        imageFile = File(path)
        uri = Uri.fromFile(imageFile)
        parcelable = cast('android.os.Parcelable', uri)
        shareIntent.putExtra(Intent.EXTRA_STREAM, parcelable)

        if app_package:
            app_package = packages[app_package] if app_package in packages else None
            try:
                shareIntent.setPackage(String(app_package))
            except JavaException:
                if call_playstore:
                    webbrowser.open(f"http://play.google.com/store/apps/details?id={app_package}")
                toast(error_msg) if error_msg else Logger.error("Kvdroid: Specified Application is unavailable")
                return

        if chooser:
            chooser = Intent.createChooser(shareIntent, String(title))
            activity.startActivity(chooser)
        else:
            activity.startActivity(shareIntent)


    def mime_type(file_path):
        return URLConnection.guessContentTypeFromName(file_path)

    def get_resource(resource):
        return autoclass(f"{activity.getPackageName()}.R${resource}")



else:
    Logger.error(
        "Kvdroid: Kvdroid is only callable for Android"
    )
