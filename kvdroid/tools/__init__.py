import contextlib
from time import sleep
from typing import Union

from kvdroid.cast import cast_object

from kvdroid import _convert_color, packages, Logger
from jnius import JavaException, autoclass  # NOQA
from kvdroid import activity
from kvdroid.jclass.androidx.core.view import ViewCompat, WindowInsetsCompatType, WindowInsetsCompat, WindowCompat
from kvdroid.jclass.java import URL, Runtime, String, Locale, URLConnection, File
from kvdroid.jclass.android import (
    Intent,
    Context,
    Environment,
    Request,
    WallpaperManager,
    Color,
    BitmapFactory,
    Rect,
    URLUtil,
    VERSION,
    ComponentName,
    Toast,
    View, ActivityInfo, Uri, Settings, TextToSpeech, WindowManagerLayoutParams, StrictMode, WindowInsetsController,
    Build, VERSION_CODES, Gravity
)
from android.runnable import run_on_ui_thread  # NOQA


def _android_version():
    version = VERSION(instantiate=True)
    return version.RELEASE


android_version = _android_version()


@run_on_ui_thread
def toast(text, length_long=False, gravity: str = "bottom", y=0, x=0):
    """
    Displays a toast.

    :param length_long: the amount of time (in seconds) that the toast is
           visible on the screen;
    :param text: text to be displayed in the toast;
    :param length_long:  duration of the toast, if `True` the toast
           will last 2.3s but if it is `False` the toast will last 3.9s;
    :param gravity: refers to the toast position, if it is 80 the toast will
           be shown below, if it is 40 the toast will be displayed above
           https://developer.android.com/reference/android/view/Gravity;
    :param y: refers to the vertical position of the toast;
    :param x: refers to the horizontal position of the toast;

    Important: if only the text value is specified and the value of
    the `gravity`, `y`, `x` parameters is not specified, their values will
    be 0 which means that the toast will be shown in the center.
    """
    gravity = getattr(Gravity(), gravity.upper()) | Gravity().CENTER_HORIZONTAL
    duration = Toast().LENGTH_SHORT if not length_long else Toast().LENGTH_LONG
    t = Toast().makeText(activity, String(text), duration)
    t.setGravity(gravity, x, y)
    t.show()


def share_text(text, title='Share', chooser=False, app_package=None, call_playstore=True, error_msg=""):
    intent = Intent(Intent().ACTION_SEND)
    intent.putExtra(Intent().EXTRA_TEXT, String(str(text)))
    intent.setType("text/plain")
    if app_package:
        app_package = packages[app_package] if app_package in packages else None
        try:
            intent.setPackage(String(app_package))
        except JavaException:
            if call_playstore:
                import webbrowser
                webbrowser.open(f"http://play.google.com/store/apps/details?id={app_package}")
            toast(error_msg) if error_msg else Logger.error("Kvdroid: Specified Application is unavailable")
            return
    from kvdroid import activity
    if chooser:
        chooser = Intent().createChooser(intent, String(title))
        activity.startActivity(chooser)
    else:
        activity.startActivity(intent)


def share_file(path, title='Share', chooser=True, app_package=None, call_playstore=True, error_msg=""):
    path = str(path)
    if VERSION().SDK_INT >= 24:
        StrictMode().disableDeathOnFileUriExposure()
    shareIntent = Intent(Intent().ACTION_SEND)
    shareIntent.setType("*/*")
    imageFile = File(path)
    uri = Uri().fromFile(imageFile)
    parcelable = cast_object('parcelable', uri)
    shareIntent.putExtra(Intent().EXTRA_STREAM, parcelable)

    if app_package:
        app_package = packages[app_package] if app_package in packages else None
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
    return URLConnection().guessContentTypeFromName(file_path)


def get_resource(resource, activity_type=activity):
    return autoclass(f"{activity_type.getPackageName()}.R${resource}")


def restart_app():
    currentActivity = cast_object('activity', activity)
    context = cast_object('context', currentActivity.getApplicationContext())
    packageManager = context.getPackageManager()
    intent = packageManager.getLaunchIntentForPackage(context.getPackageName())
    componentName = intent.getComponent()
    mainIntent = Intent().makeRestartActivityTask(componentName)
    context.startActivity(mainIntent)
    Runtime().getRuntime().exit(0)


def download_manager(title, description, url, folder=None, file_name=None):
    uri = Uri().parse(str(url))
    dm = cast_object("downloadManager", activity.getSystemService(Context().DOWNLOAD_SERVICE))
    request = Request(uri)
    request.setTitle(str(title))
    request.setDescription(str(description))
    request.setNotificationVisibility(Request().VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
    if folder and file_name:
        request.setDestinationInExternalPublicDir(str(folder), str(file_name))
    else:
        conn = URL(url).openConnection()
        with contextlib.suppress(JavaException):
            conn.getContent()
        url = conn.getURL().toString()
        print(url)
        request.setDestinationInExternalPublicDir(
            Environment().DIRECTORY_DOWNLOADS, URLUtil().guessFileName(url, None, None)
        )
    dm.enqueue(request)


@run_on_ui_thread
def change_statusbar_color(color: Union[str, list], foreground_color: str):
    color = _convert_color(color)
    window = activity.getWindow()
    if foreground_color == "black":
        if VERSION().SDK_INT >= 30:
            window_inset_controller = window.getDecorView().getWindowInsetsController()
            window_inset_controller.setSystemBarsAppearance(
                window_inset_controller.APPEARANCE_LIGHT_STATUS_BARS,
                window_inset_controller.APPEARANCE_LIGHT_STATUS_BARS
            )
        else:
            window.getDecorView().setSystemUiVisibility(
                View().SYSTEM_UI_FLAG_LIGHT_STATUS_BAR
                | window.getDecorView().getSystemUiVisibility()
            )
    elif str(foreground_color) == "white":
        if VERSION().SDK_INT >= 30:
            window_inset_controller = window.getDecorView().getWindowInsetsController()
            window_inset_controller.setSystemBarsAppearance(
                0,
                window_inset_controller.APPEARANCE_LIGHT_STATUS_BARS
            )
        else:
            window.getDecorView().setSystemUiVisibility(0)
    else:
        raise TypeError("Available options are ['white','black'] for StatusBar text color")
    if VERSION().SDK_INT <= 29:
        window.clearFlags(WindowManagerLayoutParams().FLAG_TRANSLUCENT_STATUS)
    else:
        window.setNavigationBarContrastEnforced(False)
    window.addFlags(WindowManagerLayoutParams().FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
    window.setStatusBarColor(Color().parseColor(color))


@run_on_ui_thread
def navbar_color(color: Union[str, list], foreground_color: str):
    color = _convert_color(color)
    window = activity.getWindow()
    if foreground_color == "black":
        if VERSION().SDK_INT >= 30:
            window_inset_controller = window.getDecorView().getWindowInsetsController()
            window_inset_controller.setSystemBarsAppearance(
                window_inset_controller.APPEARANCE_LIGHT_NAVIGATION_BARS,
                window_inset_controller.APPEARANCE_LIGHT_NAVIGATION_BARS
            )
        else:
            window.getDecorView().setSystemUiVisibility(
                View().SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR
                | window.getDecorView().getSystemUiVisibility()
            )
    elif foreground_color == "white":
        if VERSION().SDK_INT >= 30:
            window_inset_controller = window.getDecorView().getWindowInsetsController()
            window_inset_controller.setSystemBarsAppearance(
                0,
                window_inset_controller.APPEARANCE_LIGHT_NAVIGATION_BARS
            )
        else:
            window.getDecorView().setSystemUiVisibility(0)
    if VERSION().SDK_INT <= 29:
        window.clearFlags(WindowManagerLayoutParams().FLAG_TRANSLUCENT_NAVIGATION)
    else:
        window.setNavigationBarContrastEnforced(False)
    window.addFlags(WindowManagerLayoutParams().FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
    window.setNavigationBarColor(Color().parseColor(color))


def set_wallpaper(path_to_image):
    context = cast_object('context', activity.getApplicationContext())
    bitmap = BitmapFactory().decodeFile(path_to_image)
    manager = WallpaperManager().getInstance(context)
    return manager.setBitmap(bitmap)


def speech(text: str, lang: str):
    tts = TextToSpeech(activity, None)
    retries = 0
    tts.setLanguage(Locale(lang))
    speak_status = tts.speak(text, TextToSpeech().QUEUE_FLUSH, None)
    while retries < 100 and speak_status == -1:
        sleep(0.1)
        retries += 1
        speak_status = tts.speak(
            text, TextToSpeech().QUEUE_FLUSH, None
        )
    return speak_status


def keyboard_height():

    try:
        rect = Rect(instantiate=True)
        activity.getWindow().getDecorView().getWindowVisibleDisplayFrame(rect)
        rect.top = 0
        return activity.getWindowManager().getDefaultDisplay().getHeight() - (
            rect.bottom - rect.top
        )
    except JavaException as e:
        print(e)
        return 0


def check_keyboad_visibility_and_get_height():
    """
    https://developer.android.com/develop/ui/views/layout/sw-keyboard
    """

    view = activity.getWindow().getDecorView()
    insets = ViewCompat().getRootWindowInsets(view)
    ime_visible = insets.isVisible(WindowInsetsCompatType().ime())
    ime_height = insets.getInsets(WindowInsetsCompatType().ime()).bottom
    return ime_visible, ime_height


@run_on_ui_thread
def immersive_mode(status='enable'):
    window = activity.getWindow()
    if status == "disable":
        return window.getDecorView().setSystemUiVisibility(
            View().SYSTEM_UI_FLAG_LAYOUT_STABLE
            | View().SYSTEM_UI_FLAG_LIGHT_STATUS_BAR
            | View().SYSTEM_UI_FLAG_VISIBLE)
    else:
        return window.getDecorView().setSystemUiVisibility(
            View().SYSTEM_UI_FLAG_LAYOUT_STABLE
            | View().SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
            | View().SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
            | View().SYSTEM_UI_FLAG_HIDE_NAVIGATION
            | View().SYSTEM_UI_FLAG_FULLSCREEN
            | View().SYSTEM_UI_FLAG_IMMERSIVE_STICKY)


def launch_app_activity(app_package, app_activity):
    if int(android_version.split(".")[0]) <= 12:
        intent = Intent(Intent().ACTION_VIEW)
        intent.setClassName(app_package, app_activity)
    else:
        intent = Intent(Intent().ACTION_MAIN)
        intent.setFlags(Intent().FLAG_ACTIVITY_NEW_TASK | Intent().FLAG_ACTIVITY_RESET_TASK_IF_NEEDED)
        component_name = ComponentName(app_package, app_activity, instantiate=True)
        intent.setComponent(component_name)

    return activity.startActivity(intent)


def launch_app(app_package):
    intent = activity.getPackageManager().getLaunchIntentForPackage(app_package)
    activity.startActivity(intent)


def app_details(app_package):
    intent = Intent(Settings().ACTION_APPLICATION_DETAILS_SETTINGS)
    uri = Uri().parse(f"package:{app_package}")
    intent.setData(uri)
    activity.startActivity(intent)


def set_orientation(mode="user"):
    '''
    This function is adapted from the Pykivdroid project (https://github.com/Sahil-pixel/Pykivdroid).
    '''
    options = {
        'portrait': ActivityInfo().SCREEN_ORIENTATION_PORTRAIT,
        'landscape': ActivityInfo().SCREEN_ORIENTATION_LANDSCAPE,
        'behind': ActivityInfo().SCREEN_ORIENTATION_BEHIND,
        'full_sensor': ActivityInfo().SCREEN_ORIENTATION_FULL_SENSOR,
        'full_user': ActivityInfo().SCREEN_ORIENTATION_FULL_USER,
        'locked': ActivityInfo().SCREEN_ORIENTATION_LOCKED,
        'no_sensor': ActivityInfo().SCREEN_ORIENTATION_NOSENSOR,
        'user': ActivityInfo().SCREEN_ORIENTATION_USER,
        'user_portrait': ActivityInfo().SCREEN_ORIENTATION_USER_PORTRAIT,
        'user_landscape': ActivityInfo().SCREEN_ORIENTATION_USER_LANDSCAPE,
        'unspecified': ActivityInfo().SCREEN_ORIENTATION_UNSPECIFIED,
        'sensor_portrait': ActivityInfo().SCREEN_ORIENTATION_SENSOR_PORTRAIT,
        'sensor_landscape': ActivityInfo().SCREEN_ORIENTATION_SENSOR_LANDSCAPE,
        'sensor': ActivityInfo().SCREEN_ORIENTATION_SENSOR,
        'reverse_portrait': ActivityInfo().SCREEN_ORIENTATION_REVERSE_PORTRAIT,
        'reverse_landscape': ActivityInfo().SCREEN_ORIENTATION_REVERSE_LANDSCAPE,
    }
    with contextlib.suppress(JavaException):
        if mode in options:
            activity.setRequestedOrientation(options[mode])
