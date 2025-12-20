import contextlib
from time import sleep
from typing import Union

from kvdroid.cast import cast_object

from kvdroid import _convert_color, packages, Logger
from jnius import JavaException, autoclass  # NOQA
from kvdroid import activity
from kvdroid.jclass.androidx.core.view import (
    ViewCompat,
    WindowInsetsCompatType,
    WindowInsetsCompat,
    WindowCompat,
)
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
    View,
    ActivityInfo,
    Uri,
    Settings,
    TextToSpeech,
    WindowManagerLayoutParams,
    StrictMode,
    WindowInsetsController,
    Build,
    VERSION_CODES,
    Gravity,
)
from android.runnable import run_on_ui_thread  # NOQA


def _android_version():
    """
    Returns the version of the Android release.

    This function retrieves the release version of the Android operating system
    by instantiating a VERSION object and accessing its RELEASE attribute.

    Returns:
        str: The release version of the Android operating system.
    """
    version = VERSION(instantiate=True)
    return version.RELEASE


android_version = _android_version()


@run_on_ui_thread
def toast(text, length_long=False, gravity: str = "bottom", y=0, x=0):
    """
    Displays a toast message in an Android environment, providing a lightweight feedback
    tooltip. The gravity, duration, and position on the screen can be customized.

    Args:
        text (str): The message text to be displayed in the toast.
        length_long (bool, optional): Determines the duration of the toast. Defaults to False for a
            short duration.
        gravity (str, optional): Defines the vertical alignment of the toast. Possible options include
            "top", "bottom", "center", etc. Defaults to "bottom".
        y (int, optional): Vertical offset for the toast position. Defaults to 0.
        x (int, optional): Horizontal offset for the toast position. Defaults to 0.
    """
    gravity = getattr(Gravity(), gravity.upper()) | Gravity().CENTER_HORIZONTAL
    duration = Toast().LENGTH_SHORT if not length_long else Toast().LENGTH_LONG
    t = Toast().makeText(activity, String(text), duration)
    t.setGravity(gravity, x, y)
    t.show()


def share_text(
    text,
    title="Share",
    chooser=False,
    app_package=None,
    call_playstore=True,
    error_msg="",
):
    """
    Shares a text message using an implicit intent, allowing users to share the text
    via supported applications such as messaging apps, email clients, or social
    media apps.

    Parameters:
        text: str
            The text message to share.
        title: str, optional
            The title of the share dialog, defaults to "Share".
        chooser: bool, optional
            Whether to display a chooser dialog for app selection, defaults to False.
        app_package: str, optional
            Specific application package to directly send the text, defaults to None.
        call_playstore: bool, optional
            Whether to open the application's Play Store page if unavailable,
            defaults to True.
        error_msg: str, optional
            Custom error message to display if the specified application is unavailable,
            defaults to an empty string.
    """
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

                webbrowser.open(
                    f"http://play.google.com/store/apps/details?id={app_package}"
                )
            (
                toast(error_msg)
                if error_msg
                else Logger.error("Kvdroid: Specified Application is unavailable")
            )
            return
    from kvdroid import activity

    if chooser:
        chooser = Intent().createChooser(intent, String(title))
        activity.startActivity(chooser)
    else:
        activity.startActivity(intent)


def share_file(
    path,
    title="Share",
    chooser=True,
    app_package=None,
    call_playstore=True,
    error_msg="",
):
    """
    Shares a file with specified parameters such as title, target application, and other
    optional flags. The function uses Android's Intent system to send a file to other
    applications, enabling file sharing functionality.

    Parameters:
        path (str): The path to the file that will be shared.
        title (str, optional): The title of the chooser dialog. Defaults to "Share".
        chooser (bool, optional): A flag indicating whether to display the chooser dialog
            for selecting an app. Defaults to True.
        app_package (str, optional): The package name of the target application to share
            the file with. If not provided, allows sharing with any app.
        call_playstore (bool, optional): Determines if the Play Store should be opened if
            the specific app_package is not found. Defaults to True.
        error_msg (str, optional): The custom error message to display if the app is
            unavailable. Defaults to an empty string.

    Raises:
        None

    Returns:
        None
    """
    path = str(path)
    if VERSION().SDK_INT >= 24:
        StrictMode().disableDeathOnFileUriExposure()
    shareIntent = Intent(Intent().ACTION_SEND)
    shareIntent.setType("*/*")
    imageFile = File(path)
    uri = Uri().fromFile(imageFile)
    parcelable = cast_object("parcelable", uri)
    shareIntent.putExtra(Intent().EXTRA_STREAM, parcelable)

    if app_package:
        app_package = packages[app_package] if app_package in packages else None
        try:
            shareIntent.setPackage(String(app_package))
        except JavaException:
            if call_playstore:
                import webbrowser

                webbrowser.open(
                    f"http://play.google.com/store/apps/details?id={app_package}"
                )
            from kvdroid import Logger

            (
                toast(error_msg)
                if error_msg
                else Logger.error("Kvdroid: Specified Application is unavailable")
            )
            return

    if chooser:
        chooser = Intent().createChooser(shareIntent, String(title))
        activity.startActivity(chooser)
    else:
        activity.startActivity(shareIntent)


def mime_type(file_path):
    """
    Determines the MIME type of a file based on its name.

    This function utilizes the `URLConnection.guessContentTypeFromName`
    method to guess the MIME type of the file by its file name or extension.

    Args:
        file_path (str): The file path or name for which the MIME type
            is to be determined.

    Returns:
        str: The guessed MIME type of the file based on its name, or None
            if it cannot be determined.
    """
    return URLConnection().guessContentTypeFromName(file_path)


def get_resource_identifier(name: str, def_type: str, package_name: str = None) -> int:
    """
    Retrieves the unique resource identifier for a given resource name, type, and package.
    This function is typically used in Android development to dynamically fetch the
    resource ID needed to access resources like layouts, strings, or drawables.

    Args:
        name: The name of the resource.
        def_type: The type of the resource (e.g., "string", "drawable", "layout").
        package_name: The name of the package where the resource is located. If not provided,
            defaults to the current application's package name.

    Returns:
        int: The unique identifier of the specified resource.
    """
    if package_name is None:
        package_name = activity.getPackageName()
    return activity.getResources().getIdentifier(name, def_type, package_name)


def restart_app():
    """
    Restarts the currently running Android application by creating a new
    intent for the main activity and closing the current instance.

    Raises:
        SystemExit: Exits the runtime environment after launching the restart intent.
    """
    currentActivity = cast_object("activity", activity)
    context = cast_object("context", currentActivity.getApplicationContext())
    packageManager = context.getPackageManager()
    intent = packageManager.getLaunchIntentForPackage(context.getPackageName())
    componentName = intent.getComponent()
    mainIntent = Intent().makeRestartActivityTask(componentName)
    context.startActivity(mainIntent)
    Runtime().getRuntime().exit(0)


def download_manager(title, description, url, folder=None, file_name=None):
    """
    Manages the process of downloading a file from a given URL, and configures options
    such as title, description, destination folder, and file name. Uses Android's
    `DownloadManager` for handling downloads and notifying the user upon completion.

    Parameters:
        title (str): The title for the download notification.
        description (str): A brief description to display in the notification.
        url (str): The URL of the file to download.
        folder (Optional[str]): The optional folder where the file will be saved.
        file_name (Optional[str]): The optional name of the file to be saved.

    Raises:
        JavaException: If there's an issue with accessing or retrieving the file content.
    """
    uri = Uri().parse(str(url))
    dm = cast_object(
        "downloadManager", activity.getSystemService(Context().DOWNLOAD_SERVICE)
    )
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
def change_statusbar_color(background_color: Union[str, list], foreground_color: str):
    """
    Modifies the status bar's color and text appearance of a running application.
    It updates the background and foreground colors of the status bar depending on
    the provided parameters. It also ensures compatibility with various Android SDK
    versions using conditional handling. The method must run on the UI thread
    designated by the decorator.

    Parameters:
        background_color (Union[str, list]): The color to set as the status bar's background.
            It can be provided as a string in hexadecimal format or as a list of RGB values.
        foreground_color (str): The color for the status bar's text. Acceptable values are
            'black' or 'white'.

    Raises:
        TypeError: If the supplied foreground color is not 'black' or 'white'.
    """
    background_color = _convert_color(background_color)
    window = activity.getWindow()
    view = window.getDecorView()

    if VERSION().SDK_INT >= 30:
        window_inset_controller = view.getWindowInsetsController()
        if window_inset_controller:
            appearance = (
                window_inset_controller.APPEARANCE_LIGHT_STATUS_BARS
                if foreground_color == "black"
                else 0
            )
            window_inset_controller.setSystemBarsAppearance(
                appearance, window_inset_controller.APPEARANCE_LIGHT_STATUS_BARS
            )
    elif VERSION().SDK_INT >= 23:
        # Use bitwise logic so we don't affect the Navigation Bar flags
        current_flags = view.getSystemUiVisibility()
        if foreground_color == "black":
            new_flags = current_flags | View().SYSTEM_UI_FLAG_LIGHT_STATUS_BAR
        else:
            new_flags = current_flags & ~View().SYSTEM_UI_FLAG_LIGHT_STATUS_BAR
        view.setSystemUiVisibility(new_flags)

    # Background implementation
    window.addFlags(WindowManagerLayoutParams().FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
    if VERSION().SDK_INT <= 29:
        window.clearFlags(WindowManagerLayoutParams().FLAG_TRANSLUCENT_STATUS)
    window.setStatusBarColor(Color().parseColor(background_color))


@run_on_ui_thread
def navbar_color(background_color: Union[str, list], foreground_color: str):
    """
    Changes the navigation bar's background and foreground colors.

    This function modifies the appearance of the device's navigation bar by setting
    its background color and determining if the foreground content, such as
    navigation icons, should display in black or white.

    Parameters:
        background_color (Union[str, list]): The background color for the navigation
        bar. Can be a string representing a color (e.g., "#FFFFFF") or a list
        representing an RGB value.
        foreground_color (str): The foreground color for the navigation bar. Should
        be either "black" or "white".

    Raises:
        ValueError: If the provided background_color or foreground_color is invalid.
    """
    background_color = _convert_color(background_color)
    window = activity.getWindow()
    view = window.getDecorView()

    if VERSION().SDK_INT >= 30:
        window_inset_controller = view.getWindowInsetsController()
        if window_inset_controller:
            appearance = (
                window_inset_controller.APPEARANCE_LIGHT_NAVIGATION_BARS
                if foreground_color == "black"
                else 0
            )
            window_inset_controller.setSystemBarsAppearance(
                appearance, window_inset_controller.APPEARANCE_LIGHT_NAVIGATION_BARS
            )
    elif VERSION().SDK_INT >= 26:
        # Use bitwise logic so we don't affect the Status Bar flags
        current_flags = view.getSystemUiVisibility()
        if foreground_color == "black":
            new_flags = current_flags | View().SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR
        else:
            new_flags = current_flags & ~View().SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR
        view.setSystemUiVisibility(new_flags)

    # Background implementation
    window.addFlags(WindowManagerLayoutParams().FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
    if VERSION().SDK_INT <= 29:
        window.clearFlags(WindowManagerLayoutParams().FLAG_TRANSLUCENT_NAVIGATION)
    else:
        # Prevents Android from forcing a gray overlay on light nav bars
        window.setNavigationBarContrastEnforced(False)
    window.setNavigationBarColor(Color().parseColor(background_color))


def set_wallpaper(path_to_image):
    """
    Sets the device wallpaper to the image specified at the given file path.

    This function takes the file path of an image, decodes it into a bitmap,
    and updates the device wallpaper using the WallpaperManager.

    Args:
        path_to_image (str): The file path to the image to be set as wallpaper.

    Returns:
        bool: True if the wallpaper was set successfully, otherwise False.
    """
    context = cast_object("context", activity.getApplicationContext())
    bitmap = BitmapFactory().decodeFile(path_to_image)
    manager = WallpaperManager().getInstance(context)
    return manager.setBitmap(bitmap)


def speech(text: str, lang: str):
    """
    Performs text-to-speech conversion for the given text and language with retries in case of
    initial failure. This function utilizes the TextToSpeech class for synthesizing speech
    from text and executes up to 100 retries if the initial attempt fails.

    Parameters:
        text: str
            The text to be converted into speech.
        lang: str
            The language code (e.g., "en", "es") to be used for the text-to-speech synthesis.

    Returns:
        int
            The status code from the TextToSpeech speak method. Returns -1 if the operation fails
            after all retry attempts.
    """
    tts = TextToSpeech(activity, None)
    retries = 0
    tts.setLanguage(Locale(lang))
    speak_status = tts.speak(text, TextToSpeech().QUEUE_FLUSH, None)
    while retries < 100 and speak_status == -1:
        sleep(0.1)
        retries += 1
        speak_status = tts.speak(text, TextToSpeech().QUEUE_FLUSH, None)
    return speak_status


def keyboard_height():
    """
    Calculates the height of the keyboard in the current activity.

    This function determines the visible display frame for the current activity's
    window and calculates the height of the on-screen keyboard by measuring the
    difference between the screen height and the visible area height. If an error
    occurs in the process, it logs the exception and returns a default height value
    of 0.

    Returns:
        int: The height of the keyboard in pixels. Returns 0 if the calculation is
        unsuccessful.
    """
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


def check_keyboard_visibility_and_get_height():
    """
    Checks the visibility of the keyboard and retrieves its height.

    This function determines whether the software keyboard is visible and obtains
    its height in pixels. It uses the root window insets of the application's main
    window decor view to compute these values.

    Returns:
        tuple[bool, int]: A tuple where the first element is a boolean indicating
        whether the keyboard is visible, and the second element is an integer
        representing the height of the keyboard in pixels.
    """

    view = activity.getWindow().getDecorView()
    insets = ViewCompat().getRootWindowInsets(view)
    ime_visible = insets.isVisible(WindowInsetsCompatType().ime())
    ime_height = insets.getInsets(WindowInsetsCompatType().ime()).bottom
    return ime_visible, ime_height


@run_on_ui_thread
def immersive_mode(status="enable"):
    """
    Sets the immersive mode for an activity's window, enabling or disabling full-screen
    mode and visibility of system UI elements based on the provided status.

    Immersive mode is often used in Android applications to hide system controls,
    providing an uninterrupted and more immersive user experience.

    Parameters:
        status (str, optional): Specifies the desired status for immersive mode. Accepts "enable"
            to enable immersive mode and "disable" to disable it. Default is "enable".

    Returns:
        None
    """
    window = activity.getWindow()
    if status == "disable":
        return window.getDecorView().setSystemUiVisibility(
            View().SYSTEM_UI_FLAG_LAYOUT_STABLE
            | View().SYSTEM_UI_FLAG_LIGHT_STATUS_BAR
            | View().SYSTEM_UI_FLAG_VISIBLE
        )
    else:
        return window.getDecorView().setSystemUiVisibility(
            View().SYSTEM_UI_FLAG_LAYOUT_STABLE
            | View().SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
            | View().SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
            | View().SYSTEM_UI_FLAG_HIDE_NAVIGATION
            | View().SYSTEM_UI_FLAG_FULLSCREEN
            | View().SYSTEM_UI_FLAG_IMMERSIVE_STICKY
        )


def launch_app_activity(app_package, app_activity):
    """
    Launches an application activity on an Android device.

    This function manages launching activities with consideration of the Android
    version. It modifies the intent behavior accordingly to ensure compatibility
    with the different system versions. For Android versions 12 or below, it uses
    ACTION_VIEW, whereas for versions above 12, it uses ACTION_MAIN with specific
    flags and a component.

    Parameters:
        app_package (str): The package name of the Android application to launch.
        app_activity (str): The activity name of the application to launch.

    Returns:
        Any: The result of the activity start intent.
    """
    if int(android_version.split(".")[0]) <= 12:
        intent = Intent(Intent().ACTION_VIEW)
        intent.setClassName(app_package, app_activity)
    else:
        intent = Intent(Intent().ACTION_MAIN)
        intent.setFlags(
            Intent().FLAG_ACTIVITY_NEW_TASK
            | Intent().FLAG_ACTIVITY_RESET_TASK_IF_NEEDED
        )
        component_name = ComponentName(app_package, app_activity, instantiate=True)
        intent.setComponent(component_name)

    return activity.startActivity(intent)


def launch_app(app_package):
    """
    Launches an Android application using its package name.

    This function retrieves the launch intent for the specified application
    package and starts the application using the Android activity context.

    Parameters:
    app_package (str): The package name of the Android application to launch.

    Raises:
    None
    """
    intent = activity.getPackageManager().getLaunchIntentForPackage(app_package)
    activity.startActivity(intent)


def app_details(app_package):
    """
    Opens the application details settings for a specified app package.

    This function creates an intent to navigate to the application details of
    a given package using the system settings.

    Args:
        app_package: str
            The package name of the application to open the details
            settings for.
    """
    intent = Intent(Settings().ACTION_APPLICATION_DETAILS_SETTINGS)
    uri = Uri().parse(f"package:{app_package}")
    intent.setData(uri)
    activity.startActivity(intent)


def set_orientation(mode="user"):
    """
    Sets the screen orientation of the activity based on the provided mode.

    This function assigns a specific orientation to the activity based on the input
    mode. It utilizes a mapping of modes to predefined constants from the
    ActivityInfo class to set the requested orientation. If the mode is invalid or
    an exception occurs, the function suppresses the exception gracefully.

    Parameters:
        mode: str
            The desired screen orientation mode. Available modes include:
            'portrait', 'landscape', 'behind', 'full_sensor', 'full_user',
            'locked', 'no_sensor', 'user', 'user_portrait', 'user_landscape',
            'unspecified', 'sensor_portrait', 'sensor_landscape', 'sensor',
            'reverse_portrait', and 'reverse_landscape'. Defaults to 'user'.

    Raises:
        None. Any exceptions are suppressed.
    """
    options = {
        "portrait": ActivityInfo().SCREEN_ORIENTATION_PORTRAIT,
        "landscape": ActivityInfo().SCREEN_ORIENTATION_LANDSCAPE,
        "behind": ActivityInfo().SCREEN_ORIENTATION_BEHIND,
        "full_sensor": ActivityInfo().SCREEN_ORIENTATION_FULL_SENSOR,
        "full_user": ActivityInfo().SCREEN_ORIENTATION_FULL_USER,
        "locked": ActivityInfo().SCREEN_ORIENTATION_LOCKED,
        "no_sensor": ActivityInfo().SCREEN_ORIENTATION_NOSENSOR,
        "user": ActivityInfo().SCREEN_ORIENTATION_USER,
        "user_portrait": ActivityInfo().SCREEN_ORIENTATION_USER_PORTRAIT,
        "user_landscape": ActivityInfo().SCREEN_ORIENTATION_USER_LANDSCAPE,
        "unspecified": ActivityInfo().SCREEN_ORIENTATION_UNSPECIFIED,
        "sensor_portrait": ActivityInfo().SCREEN_ORIENTATION_SENSOR_PORTRAIT,
        "sensor_landscape": ActivityInfo().SCREEN_ORIENTATION_SENSOR_LANDSCAPE,
        "sensor": ActivityInfo().SCREEN_ORIENTATION_SENSOR,
        "reverse_portrait": ActivityInfo().SCREEN_ORIENTATION_REVERSE_PORTRAIT,
        "reverse_landscape": ActivityInfo().SCREEN_ORIENTATION_REVERSE_LANDSCAPE,
    }
    with contextlib.suppress(JavaException):
        if mode in options:
            activity.setRequestedOrientation(options[mode])
