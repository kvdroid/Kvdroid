from typing import Union
from kvdroid import _convert_color
from jnius import JavaException
from kvdroid import activity
from kvdroid.jclass.android import Intent, Context
from kvdroid.jclass.android.app import Request, WallpaperManager
from kvdroid.jclass.android.graphics import Color, BitmapFactory, Rect
from android.runnable import run_on_ui_thread # NOQA


def toast(message):
    return activity.toastError(str(message))


def share_text(text, title='Share', chooser=False, app_package=None, call_playstore=True, error_msg=""):
    intent = Intent(Intent().ACTION_SEND)  # a function call that returns a java class call
    from kvdroid.jclass.java import String
    intent.putExtra(Intent().EXTRA_TEXT, String(str(text)))
    intent.setType("text/plain")
    if app_package:
        from kvdroid import packages
        app_package = packages[app_package] if app_package in packages else None
        from jnius import JavaException
        try:
            intent.setPackage(String(app_package))
        except JavaException:
            if call_playstore:
                import webbrowser
                webbrowser.open(f"http://play.google.com/store/apps/details?id={app_package}")
            from kvdroid import Logger
            toast(error_msg) if error_msg else Logger.error("Kvdroid: Specified Application is unavailable")
            return
    from kvdroid import activity
    if chooser:
        chooser = Intent().createChooser(intent, String(title))
        activity.startActivity(chooser)
    else:
        activity.startActivity(intent)


def share_file(path, title='Share', chooser=True, app_package=None, call_playstore=True, error_msg=""):
    from kvdroid.jclass.java import String
    path = str(path)
    from kvdroid.jclass.android import VERSION
    if VERSION().SDK_INT >= 24:
        from kvdroid.jclass.android import StrictMode
        StrictMode().disableDeathOnFileUriExposure()
    shareIntent = Intent(Intent().ACTION_SEND)
    shareIntent.setType("*/*")
    from kvdroid.jclass.java import File
    imageFile = File(path)
    from kvdroid.jclass.android import Uri
    uri = Uri().fromFile(imageFile)
    from kvdroid.cast import cast_object
    parcelable = cast_object('parcelable', uri)
    shareIntent.putExtra(Intent().EXTRA_STREAM, parcelable)

    if app_package:
        from kvdroid import packages
        app_package = packages[app_package] if app_package in packages else None
        from jnius import JavaException
        try:
            shareIntent.setPackage(String(app_package))
        except JavaException:
            if call_playstore:
                import webbrowser
                webbrowser.open(f"http://play.google.com/store/apps/details?id={app_package}")
            from kvdroid import Logger
            toast(error_msg) if error_msg else Logger.error("Kvdroid: Specified Application is unavailable")
            return

    if chooser:
        chooser = Intent().createChooser(shareIntent, String(title))
        activity.startActivity(chooser)
    else:
        activity.startActivity(shareIntent)


def mime_type(file_path):
    from kvdroid.jclass.java import URLConnection
    return URLConnection().guessContentTypeFromName(file_path)


def get_resource(resource, activity_type=activity):
    from jnius import autoclass
    return autoclass(f"{activity_type.getPackageName()}.R${resource}")


def restart_app():
    from kvdroid.cast import cast_object
    currentActivity = cast_object('activity', activity)
    context = cast_object('context', currentActivity.getApplicationContext())
    packageManager = context.getPackageManager()
    intent = packageManager.getLaunchIntentForPackage(context.getPackageName())
    componentName = intent.getComponent()
    mainIntent = Intent().makeRestartActivityTask(componentName)
    context.startActivity(mainIntent)
    from kvdroid.jclass.java.lang import Runtime
    Runtime().getRuntime().exit(0)


def download_manager(title, description, url, folder, file_name):
    from kvdroid.jclass.android import Uri
    uri = Uri().parse(str(url))
    from kvdroid.cast import cast_object
    dm = cast_object("downloadManager", activity.getSystemService(Context().DOWNLOAD_SERVICE))
    request = Request(uri)
    request.setTitle(str(title))
    request.setDescription(str(description))
    request.setNotificationVisibility(Request().VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
    request.setDestinationInExternalPublicDir(str(folder), str(file_name))
    dm.enqueue(request)


@run_on_ui_thread
def change_statusbar_color(color: Union[str, list], text_color):
    color = _convert_color(color)
    window = activity.getWindow()
    if str(text_color) == "black":
        from kvdroid.jclass.android import View
        window.getDecorView().setSystemUiVisibility(View().SYSTEM_UI_FLAG_LIGHT_STATUS_BAR)
    elif str(text_color) == "white":
        window.getDecorView().setSystemUiVisibility(0)
    else:
        raise TypeError("Available options are ['white','black'] for StatusBar text color")
    from kvdroid.jclass.android import LayoutParams
    window.clearFlags(LayoutParams().FLAG_TRANSLUCENT_STATUS)
    window.addFlags(LayoutParams().FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
    window.setStatusBarColor(Color().parseColor(color))


@run_on_ui_thread
def navbar_color(color: Union[str, list]):
    color = _convert_color(color)
    window = activity.getWindow()
    window.setNavigationBarColor(Color().parseColor(color))


def set_wallpaper(path_to_image):
    from kvdroid.cast import cast_object
    context = cast_object('context', activity.getApplicationContext())
    from kvdroid.jclass.java import File
    file = File(str(path_to_image))
    bitmap = BitmapFactory().decodeFile(file.getAbsolutePath())
    manager = WallpaperManager().getInstance(context)
    return manager.setBitmap(bitmap)


def speech(text, lang):
    from kvdroid.jclass.android.speech.tts import TextToSpeech
    tts = TextToSpeech(activity, None)
    from kvdroid.jclass.java.util import Locale
    tts.setLanguage(Locale(str(lang)))
    return tts.speak(str(text), TextToSpeech().QUEUE_FLUSH, None)


def keyboard_height():
    try:
        decor_view = activity.getWindow().getDecorView()
        height = activity.getWindowManager().getDefaultDisplay().getHeight()
        decor_view.getWindowVisibleDisplayFrame(Rect)
        return height - Rect().bottom
    except JavaException:
        return 0


@run_on_ui_thread
def immersive_mode():
    window = activity.getWindow()
    from kvdroid.jclass.android import View
    View = View()
    return window.getDecorView().setSystemUiVisibility(
        View.SYSTEM_UI_FLAG_LAYOUT_STABLE
        | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
        | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
        | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
        | View.SYSTEM_UI_FLAG_FULLSCREEN
        | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY)


def launch_app_internally(app_package, app_activity):
    intent = Intent(Intent().ACTION_VIEW)
    intent.setClassName(app_package, app_activity)
    return activity.startActivity(intent)


def launch_app_externally(app_package):
    intent = activity.getPackageManager().getLaunchIntentForPackage(app_package)
    activity.startActivity(intent)


def app_details(app_package):
    from kvdroid.jclass.android import Settings
    intent = Intent(Settings().ACTION_APPLICATION_DETAILS_SETTINGS)
    from kvdroid.jclass.android import Uri
    uri = Uri().parse("package:" + app_package)
    intent.setData(uri)
    activity.startActivity(intent)
