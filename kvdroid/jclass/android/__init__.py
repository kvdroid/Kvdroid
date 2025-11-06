from .content.res import *
from .content import *
from .speech.tts import *
from .speech import *
from .app import *
from .graphics import *
from .graphics.drawable import *
from .location import *
from .media import *
from .net import *
from .os import *
from .os.ext import *
from .provider import *
from .view import *
from .webkit import *
from .widget import *
from .net.wifi import *
from .text.format import *
from .hardware.camera2 import *
from .hardware.camera2.params import *
from .support.v4.app import *
from .content.pm import *
from .R import *
from .telephony import *
from .util import *

from jnius import autoclass
from kvdroid.jclass import _class_call


def Manifest(*args, instantiate: bool = False):
    return _class_call(autoclass("android.Manifest"), args, instantiate)


