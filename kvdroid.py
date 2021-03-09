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
        
    except BaseException:
        Logger.error(
            "Kvdroid: Cannot load classes by Pyjnius. Make sure requirements installed"
        )

    def app_source():
        packageName = activity.getPackageName()
        installer =  activity.getPackageManager().getInstallerPackageName(packageName)
        if installer == "com.android.vending":
            return "playstore"
        else:
            return "unknown"
    app_source = app_source()
    """To detect if target app installed from PlayStore or not
    from kvdroid import app_source
    print(app_source)
    >> playstore"""

    class Metrics(object):
        config = activity.getResources().getConfiguration()
        metric = activity.getResources().getDisplayMetrics()  
          
        def height_dp(self):
            return self.config.screenHeightDp
                    
        def width_dp(self):
            return self.config.screenWidthDp 
                   
        def height_px(self):
             return self.metric.heightPixels
             
        def width_px(self):
             return self.metric.widthPixels
             
        def orientation(self):
            if self.config.orientation == 1:
                 return "potrait"
            else:
                 return "landscape"
    screen  = Metrics()
    """To get screen size in dp or pixel and detect current orientation
    from kvdroid import screen
    print(screen.orientation())
    >> potrait"""
    
    def network_state():
        ConnectivityManager = autoclass('android.net.ConnectivityManager')
        con_mgr = activity.getSystemService(AndroidActivity.CONNECTIVITY_SERVICE)
        conn = con_mgr.getNetworkInfo(ConnectivityManager.TYPE_WIFI).isConnectedOrConnecting()
        try:
            if conn:
                return True
            else:
                conn = con_mgr.getNetworkInfo(ConnectivityManager.TYPE_MOBILE).isConnectedOrConnecting()
                if conn:
                    return True
                else:
                    return False
        except:
             return False
    network_state = network_state()
    """To check if device has a data connection both for wifi and cellular
    from kvdroid import network_state
    print(network_state)"""
    
    def dark_mode():
        config = activity.getResources().getConfiguration()
        Configuration = autoclass("android.content.res.Configuration")
        night_mode_flags = activity.getContext().getResources().getConfiguration().uiMode & Configuration.UI_MODE_NIGHT_MASK
        if night_mode_flags == Configuration.UI_MODE_NIGHT_YES:
    	    return True
        elif night_mode_flags == Configuration.UI_MODE_NIGHT_NO:
            return False
        elif night_mode_flags == Configuration.UI_MODE_NIGHT_UNDEFINED:
            return False
    dark_mode = dark_mode()
    """To check if device is  in dark mode or not
    from kvdroid import dark_mode
    print(dark_mode)"""
        
    def device_info(yaz):
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
            'sdk_int': VERSION.SDK_INT
        }
        return os[yaz]
    """To get device's informations
    from kvdroid import device_info
    print(device_info("model"))"""
    

    @run_on_ui_thread
    def immersive_mode(immerse = None):
        if not immerse:
            pass
        else:
            if immerse == True:
            	window = activity.getWindow()
            	return window.getDecorView().setSystemUiVisibility(
                        View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                            | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                            | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                            | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                            | View.SYSTEM_UI_FLAG_FULLSCREEN
                            | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY)
            else:
                window = activity.getWindow()
                return window.getDecorView().setSystemUiVisibility(
                        View.SYSTEM_UI_FLAG_VISIBLE)
                            
    """To enable immersive mode
    from kvdroid import immersive_mode
    immersive_mode(True)"""
       
    def launch_app(app_package, app_activity):
        Intent = autoclass('android.content.Intent')
        intent = Intent()
        intent.setAction(Intent.ACTION_VIEW)    
        intent.setClassName(app_package, app_activity)
        return activity.startActivity(intent)
        
    """To launch a specific app
    from kvdroid import launch_app  
    launch_app(<app_package>,<app_activity>)"""
    
    def app_details(app_package):
        Provider = autoclass('android.provider.Settings')
        Uri = autoclass('android.net.Uri')
        Intent = autoclass('android.content.Intent')
        intent = Intent()
        intent.setAction(Provider.ACTION_APPLICATION_DETAILS_SETTINGS)    
        uri = Uri.parse("package:"+app_package)           
        intent.setData(uri)
        activity.startActivity(intent)
        
    """To open target app's details page
    from kvdroid import app_details
    app_details(<app_package>)"""
    
    def device_lang():
        Locale = autoclass('java.util.Locale')
        return Locale.getDefault().getLanguage()
    device_lang = device_lang()
    """To detect current device's language
    from kvdroid import device_lang
    print(device_lang)"""

    @run_on_ui_thread
    def statusbar_color(color,text_color):
    	window = activity.getWindow()
    	if str(text_color) == "black":
    	    window.getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR)
    	elif str(text_color) == "white":
    	    window.getDecorView().setSystemUiVisibility(0)
    	else:
    	    raise  TypeError("Available options are ['white','black'] for StatusBar text color")
    	window.clearFlags(WindowManager.FLAG_TRANSLUCENT_STATUS)
    	window.addFlags(WindowManager.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
    	window.setStatusBarColor(Color.parseColor(str(color)))
    """To deternine statusbar color
    from kvdroid import statusbar_color
    statusbar_color("#FFFFFF","black")"""
    
    @run_on_ui_thread
    def navbar_color(color):
        window = activity.getWindow()
        window.setNavigationBarColor(Color.parseColor(str(color)))
    """To deternine navigationbar color
    from kvdroid import nav_bar_color
    navbar_color("#FFFFFF")"""
    
    def toast(message):
        return PythonActivity.toastError(str(message))
    """To show a toast message
    from kvdroid import toast
    toast("hello world")"""
    
    def sdcard():
    	Environment = autoclass("android.os.Environment")
    	return Environment.getExternalStorageDirectory().toString()
    sdcard = sdcard()
    """To get absolute sdcard path
    from kvdroid import sdcard
    print(sdcard)"""

    def path():
        import os
        return os.path.dirname(os.path.abspath(__file__))
    app_folder = path()
    """To get path of working app folder
    from kvdroid import app_folder
    print(app_folder)"""

    def set_wallpaper(path_to_image):
        context = cast('android.content.Context', activity.getApplicationContext())	
        File = autoclass('java.io.File')
        file = File(str(path_to_image))	
        BitmapFactory = autoclass('android.graphics.BitmapFactory')
        bitmap = BitmapFactory.decodeFile(file.getAbsolutePath())	
        WallpaperManager = autoclass('android.app.WallpaperManager')
        manager = WallpaperManager.getInstance(context)
        return manager.setBitmap(bitmap)
    """To change default wallpaper
    from kvdroid import wallpaper
    set_wallpaper("/sdcard/test.jpg")"""

    def speech(text,lang):
        Locale = autoclass('java.util.Locale')
        TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
        tts = TextToSpeech(activity, None)
        tts.setLanguage(Locale(str(lang)))
        return tts.speak(str(text), TextToSpeech.QUEUE_FLUSH, None)
    """To use text to speech
    from kvdroid import speech
    speech("hello world", "en")"""
    
    def download_manager(title,description,url,folder,file_name):
        Context = autoclass('android.content.Context')
        Uri = autoclass('android.net.Uri')    
        Request = autoclass("android.app.DownloadManager$Request")
        uri = Uri.parse(str(url))
        dm = cast("android.app.DownloadManager",activity.getSystemService(Context.DOWNLOAD_SERVICE))
        request = Request(uri)
        request.setTitle(str(title))
        request.setDescription(str(description))
        request.setNotificationVisibility(Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
        request.setDestinationInExternalPublicDir(str(folder), str(file_name))
        dm.enqueue(request)
    """To use default download manager
    from kvdroid import download_manager
    download_manager(<title>,<description>,<URL>,<path>,<file>)"""

    def restart_app(restart=False):
        if not restart:
            pass
        else:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Runtime = autoclass('java.lang.Runtime')
            intent = Intent()
            currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
            context = cast('android.content.Context', currentActivity.getApplicationContext())
            packageManager = context.getPackageManager()
            intent = packageManager.getLaunchIntentForPackage(context.getPackageName())
            componentName = intent.getComponent()
            mainIntent = Intent.makeRestartActivityTask(componentName)
            context.startActivity(mainIntent)
            Runtime.getRuntime().exit(0)
    """To restart the app
    from kvdroid import restart_app
    restart_app(True)"""
       
    def share_text(text):
        Intent = autoclass('android.content.Intent')
        String = autoclass("java.lang.String")
        intent = Intent()
        intent.setAction(Intent.ACTION_SEND)
        intent.putExtra(Intent.EXTRA_TEXT, String(str(text)))
        intent.setType("text/plain")
        chooser = Intent.createChooser(intent, String('Share'))
        activity.startActivity(chooser)
    """To share text via Android Share menu
    from kvdroid import share_text
    share_text(<str>)"""
   
    def share_file(text):
        path = str(text)
        StrictMode = autoclass('android.os.StrictMode')
        StrictMode.disableDeathOnFileUriExposure()    
        Intent = autoclass('android.content.Intent')
        String = autoclass('java.lang.String')
        Uri = autoclass('android.net.Uri')
        File = autoclass('java.io.File')    
        shareIntent = Intent(Intent.ACTION_SEND)
        shareIntent.setType("*/*")    
        imageFile = File(path)
        uri = Uri.fromFile(imageFile)
        parcelable = cast('android.os.Parcelable', uri)
        shareIntent.putExtra(Intent.EXTRA_STREAM, parcelable)    
        currentActivity = cast('android.app.Activity', activity)
        currentActivity.startActivity(shareIntent)
    """To share any file via Android Share menu
    from kvdroid import share_file
    share_file(<path-and-file>)
    share_file("/sdcard/test.pdf")"""  

    class Player(object):
        MediaPlayer = autoclass('android.media.MediaPlayer')
        AudioManager = autoclass('android.media.AudioManager')
        mPlayer = MediaPlayer()                
        def raw(self):
            return self.mPlayer
        
        def play(self,content):
            self.content = str(content)
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
            
        def stream(self,content):
            self.content = str(content)
            self.mPlayer.setAudioStreamType(self.AudioManager.STREAM_MUSIC)
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
            
        def current_possition(self):
            if self.content: 
                return self.mPlayer.getCurrentPosition()
            
        def seek(self,value):
            try:
                self.mPlayer.seekTo(int(value) * 1000)
            except:
                pass
            
        def do_loop(self,loop = False):
            if not loop:
                self.mPlayer.setLooping(False)
            else:
                self.mPlayer.setLooping(True)
                
        def is_playing(self):
            if self.mPlayer.isPlaying == True:
                return True
            else:
                return False        
    player = Player()
    """To play suported music or radio stream through Android Media Player
    from kvdroid import player
    player.play(<path-to-music-file>)
    player.raw == Andriod Media Player"""

else:
    Logger.error(
        "Kvdroid: Kvdroid is only callable for Android"
    )