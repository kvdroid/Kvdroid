from kvdroid import activity, Configuration


def dark_mode():
    config = activity.getResources().getConfiguration()
    night_mode_flags = activity.getContext().getResources().getConfiguration().uiMode & Configuration.UI_MODE_NIGHT_MASK
    if night_mode_flags == Configuration.UI_MODE_NIGHT_YES:
      return True
    elif night_mode_flags == Configuration.UI_MODE_NIGHT_NO:
        return False
    elif night_mode_flags == Configuration.UI_MODE_NIGHT_UNDEFINED:
        return False
dark_mode = dark_mode()
