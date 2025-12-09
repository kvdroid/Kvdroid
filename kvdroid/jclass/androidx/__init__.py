from jnius import autoclass, JavaException


try:
    autoclass("androidx.core.app.ActivityCompat")
except JavaException as e:
    raise JavaException(
        f"{e}\nadd androidx.appcompat:appcompat:1.7.1 and org.jetbrains.kotlin:kotlin-stdlib-jdk8:1.8.0"
        f" to buildozer.spec file: android.gradle_dependencies. Make sure your target API is 36 or higher."
    )

from .browser.customtabs import *
from .core.app import *
from .core.content import *
from .core.view import *
from .activity import *
from .appcompat.app import *
from .core.view import *
from .media3.exoplayer import *
from .media3.common import *
from .media3.session import *
