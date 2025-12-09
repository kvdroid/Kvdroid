from typing import Callable
from jnius import PythonJavaClass, java_method
from enum import Enum
from kvdroid.jclass.androidx import WindowInsetsCompatType, WindowInsetsCompat


class WindowInsetsType(Enum):
    SYSTEM_BARS = "systemBars"
    SYSTEM_GESTURES = "systemGestures"
    MANDATORY_SYSTEM_GESTURES = "mandatorySystemGestures"
    TAPPABLE_ELEMENT = "tappableElement"
    DISPLAY_CUTOUT = "displayCutout"


class Insets:
    __slots__ = ("insets",)

    def __init__(self, insets):
        self.insets = insets

    @property
    def top(self):
        return self.insets.top

    @property
    def bottom(self):
        return self.insets.bottom

    @property
    def left(self):
        return self.insets.left

    @property
    def right(self):
        return self.insets.right


class OnApplyWindowInsetsListener(PythonJavaClass):
    __javainterfaces__ = ["androidx/core/view/OnApplyWindowInsetsListener"]
    __javacontext__ = "app"

    def __init__(
        self,
        callback: Callable[[Insets], None],
        insets_type: (
            WindowInsetsType | tuple[WindowInsetsType, WindowInsetsType]
        ) = WindowInsetsType.SYSTEM_BARS,
    ):
        super().__init__()
        self.callback = callback
        self.insets_type = insets_type
        self.__CONSUMED = WindowInsetsCompat().CONSUMED

    @java_method(
        "(Landroid/view/View;Landroidx/core/view/WindowInsetsCompat;)Landroidx/core/view/WindowInsetsCompat;"
    )
    def onApplyWindowInsets(self, _, window_insets):
        """
        v: android.view.View
        window_insets: android.view.WindowInsets
        returns: android.view.WindowInsets
        """

        if isinstance(self.insets_type, tuple):
            inset_type = (
                getattr(WindowInsetsCompatType(), self.insets_type[0].value)()
                | getattr(WindowInsetsCompatType(), self.insets_type[1].value)()
            )
        else:
            inset_type = getattr(WindowInsetsCompatType(), self.insets_type.value)()
        insets = window_insets.getInsets(inset_type)
        self.callback(Insets(insets))

        return self.__CONSUMED
