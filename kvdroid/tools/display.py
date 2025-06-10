from kvdroid.jclass.androidx import WindowCompat
from kvdroid import activity
from android.runnable import run_on_ui_thread  # noqa


@run_on_ui_thread
def set_edge_to_edge():
    # https://developer.android.com/develop/ui/views/layout/edge-to-edge-manually#java
    WindowCompat().setDecorFitsSystemWindows(activity.getWindow(), False)


def get_statusbar_height():
    # https://gist.github.com/hamakn/8939eb68a920a6d7a498
    statusbar_height = 0
    resource_id = activity.getResources().getIdentifier("status_bar_height", "dimen", "android")
    if resource_id > 0:
        statusbar_height = activity.getResources().getDimensionPixelSize(resource_id)
    return statusbar_height


def get_navbar_height():
    # https://gist.github.com/hamakn/8939eb68a920a6d7a498
    navbar_height = 0
    resource_id = activity.getResources().getIdentifier("navigation_bar_height", "dimen", "android")
    if resource_id > 0:
        navbar_height = activity.getResources().getDimensionPixelSize(resource_id)
    return navbar_height


@run_on_ui_thread
def set_appearance_light_navigation_bars(is_light=True):
    # https://developer.android.com/develop/ui/views/layout/edge-to-edge-manually#java
    window = activity.getWindow()
    window_inset_controller = WindowCompat().getInsetsController(window, window.getDecorView())
    # if not window_inset_controller:
    #     return
    window_inset_controller.setAppearanceLightNavigationBars(is_light)


@run_on_ui_thread
def set_appearance_light_status_bars(is_light=True):
    # https://developer.android.com/develop/ui/views/layout/edge-to-edge-manually#java
    window = activity.getWindow()
    window_inset_controller = WindowCompat().getInsetsController(window, window.getDecorView())
    # if not window_inset_controller:
    #     return
    window_inset_controller.setAppearanceLightStatusBars(is_light)


def set_appearance_all_bar(is_light=True):
    set_appearance_light_navigation_bars(is_light)
    set_appearance_light_status_bars(is_light)
