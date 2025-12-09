import logging
from os import environ
from typing import Union

from jnius import autoclass  # NOQA
import functools
import inspect


def _get_platform():
    # On Android sys.platform returns 'linux2', so prefer to check the
    # existence of environ variables set during Python initialization
    kivy_build = environ.get("KIVY_BUILD", "")
    if kivy_build in {"android", "ios"}:
        return kivy_build
    elif "P4A_BOOTSTRAP" in environ or "ANDROID_ARGUMENT" in environ:
        return "android"
    return None


def get_hex_from_color(color: list):
    return "#" + "".join([f"{int(i * 255):02x}" for i in color])


def _convert_color(color: Union[str, list]):
    if isinstance(color, list):
        color = get_hex_from_color(color)
    return color


platform = _get_platform()
Logger = logging.getLogger("kvdroid")

if platform != "android":
    raise ImportError("Kvdroid: Kvdroid is only callable from Android")
from android.config import ACTIVITY_CLASS_NAME, SERVICE_CLASS_NAME  # NOQA

if "PYTHON_SERVICE_ARGUMENT" in environ:
    PythonService = autoclass(SERVICE_CLASS_NAME)
    activity = PythonService.mService
else:
    PythonActivity = autoclass(ACTIVITY_CLASS_NAME)
    activity = PythonActivity.mActivity

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
    "snapchat": "com.snapchat.android",
    "chrome": "com.android.chrome",
}


def get_android_sdk_int():
    """Returns the actual Android SDK_INT for demonstration purposes."""
    return autoclass("android.os.Build$VERSION").SDK_INT


# --- Core Decorator Logic ---


def require_api(operator: str, target_sdk: int):
    """
    A decorator factory to create a decorator that checks the current Android SDK_INT
    against a target value using a specified comparison operator.

    Args:
        operator (str): The comparison operator (e.g., '>', '<', '>=', '<=', '==', '!=').
        target_sdk (int): The SDK integer value to compare against.
    """

    current_sdk = get_android_sdk_int()

    # 1. Define the Comparison Function
    def compare(sdk_int):
        """Performs the actual comparison based on the factory's settings."""
        if operator == ">":
            return sdk_int > target_sdk
        elif operator == "<":
            return sdk_int < target_sdk
        elif operator == ">=":
            return sdk_int >= target_sdk
        elif operator == "<=":
            return sdk_int <= target_sdk
        elif operator == "==":
            return sdk_int == target_sdk
        elif operator == "!=":
            return sdk_int != target_sdk
        else:
            raise ValueError(f"Invalid operator '{operator}'.")

    # 2. Define the Wrapper Function (The actual decorator)
    def decorator(obj):

        # Determine if the current SDK meets the required criteria
        is_compatible = compare(current_sdk)

        # If compatible, return the original object (function/method/class)
        if is_compatible:
            # For logging/debugging: print(f"SDK {current_sdk} is compatible with {operator} {target_sdk}")
            return obj

        # --- Incompatible Handling ---

        # Check if the object is a Class
        if inspect.isclass(obj):
            # If the class is incompatible, replace it with a dummy class
            # This dummy class raises a useful error upon instantiation or access.
            @functools.wraps(obj, updated=())
            class IncompatibleClass:
                def __init__(self, *args, **kwargs):
                    raise RuntimeError(
                        f"Cannot instantiate class '{obj.__name__}'. "
                        f"Requires SDK {operator} {target_sdk}, but current SDK is {current_sdk}."
                    )

                def __getattr__(self, name):
                    raise RuntimeError(
                        f"Cannot access member '{name}' of class '{obj.__name__}'. "
                        f"Requires SDK {operator} {target_sdk}, but current SDK is {current_sdk}."
                    )

            return IncompatibleClass

        # Check if the object is a Function or Method
        elif inspect.isfunction(obj) or inspect.ismethod(obj):

            # Replace the function/method with a placeholder that raises an error
            @functools.wraps(obj)
            def incompatible_placeholder(*args, **kwargs):
                raise NotImplementedError(
                    f"Function/Method '{obj.__name__}' is unavailable. "
                    f"Requires SDK {operator} {target_sdk}, but current SDK is {current_sdk}."
                )

            return incompatible_placeholder

        else:
            # Fallback for unexpected types
            return obj  # Or raise an error

    # Return the actual decorator function
    return decorator
