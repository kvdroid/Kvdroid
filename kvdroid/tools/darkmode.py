from kvdroid import activity


def dark_mode():
    from kvdroid.jclass.android import Configuration
    Configuration = Configuration()
    night_mode_flags = activity.getContext().getResources().getConfiguration().uiMode & Configuration.UI_MODE_NIGHT_MASK
    if night_mode_flags == Configuration.UI_MODE_NIGHT_YES:
        return True
    elif night_mode_flags in [
        Configuration.UI_MODE_NIGHT_NO,
        Configuration.UI_MODE_NIGHT_UNDEFINED,
    ]:
        return False
