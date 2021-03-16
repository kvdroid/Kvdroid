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
        
    def keyboard_height():
        try:
            rctx = autoclass('android.graphics.Rect')()
            decor_view = activity.getWindow().getDecorView()
            height = activity.getWindowManager().getDefaultDisplay().getHeight()
            decor_view.getWindowVisibleDisplayFrame(rctx)
            return height - rctx.bottom
        except:
            return 0
    keyboard_height = keyboard_height()
            

    def app_source():
        packageName = activity.getPackageName()
        installer =  activity.getPackageManager().getInstallerPackageName(packageName)
        if installer == "com.android.vending":
            return "playstore"
        else:
            return "unknown"
    app_source = app_source()

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
                            
       
    def launch_app(app_package, app_activity):
        Intent = autoclass('android.content.Intent')
        intent = Intent()
        intent.setAction(Intent.ACTION_VIEW)    
        intent.setClassName(app_package, app_activity)
        return activity.startActivity(intent)

    
    def app_details(app_package):
        Provider = autoclass('android.provider.Settings')
        Uri = autoclass('android.net.Uri')
        Intent = autoclass('android.content.Intent')
        intent = Intent()
        intent.setAction(Provider.ACTION_APPLICATION_DETAILS_SETTINGS)    
        uri = Uri.parse("package:"+app_package)           
        intent.setData(uri)
        activity.startActivity(intent)
    
    def device_lang():
        Locale = autoclass('java.util.Locale')
        return Locale.getDefault().getLanguage()
    device_lang = device_lang()

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
    
    @run_on_ui_thread
    def navbar_color(color):
        window = activity.getWindow()
        window.setNavigationBarColor(Color.parseColor(str(color)))
    
    def toast(message):
        return PythonActivity.toastError(str(message))

    def sdcard():
    	Environment = autoclass("android.os.Environment")
    	return Environment.getExternalStorageDirectory().toString()
    sdcard = sdcard()

    def path():
        import os
        return os.path.dirname(os.path.abspath(__file__))
    app_folder = path()

    def set_wallpaper(path_to_image):
        context = cast('android.content.Context', activity.getApplicationContext())	
        File = autoclass('java.io.File')
        file = File(str(path_to_image))	
        BitmapFactory = autoclass('android.graphics.BitmapFactory')
        bitmap = BitmapFactory.decodeFile(file.getAbsolutePath())	
        WallpaperManager = autoclass('android.app.WallpaperManager')
        manager = WallpaperManager.getInstance(context)
        return manager.setBitmap(bitmap)

    def speech(text,lang):
        Locale = autoclass('java.util.Locale')
        TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
        tts = TextToSpeech(activity, None)
        tts.setLanguage(Locale(str(lang)))
        return tts.speak(str(text), TextToSpeech.QUEUE_FLUSH, None)
    
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
       
    def share_text(text):
        Intent = autoclass('android.content.Intent')
        String = autoclass("java.lang.String")
        intent = Intent()
        intent.setAction(Intent.ACTION_SEND)
        intent.putExtra(Intent.EXTRA_TEXT, String(str(text)))
        intent.setType("text/plain")
        chooser = Intent.createChooser(intent, String('Share'))
        activity.startActivity(chooser)
   
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

else:
    Logger.error(
        "Kvdroid: Kvdroid is only callable for Android"
    )