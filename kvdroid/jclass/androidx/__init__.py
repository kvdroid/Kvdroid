from jnius import autoclass, JavaException


try:
    autoclass("androidx.core.app.ActivityCompat")
except JavaException as e:
    raise JavaException(
        f"{e}\nadd androidx.appcompat:appcompat:1.4.2 to buildozer.spec file: android.gradle_dependencies")

from .browser.customtabs import *
from .core.app import *
from .core.content import *
from .activity import *
from .appcompat.app import *
from .core.view import *
from .media3.exoplayer import *
from .media3.common import *
