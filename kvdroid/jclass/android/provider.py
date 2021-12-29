from jnius import autoclass
from kvdroid.jclass import _class_call


def Settings(*args, instantiate: bool = False):
    return _class_call(autoclass('android.provider.Settings'), args, instantiate)


def Contacts(*args, instantiate: bool = False):
    return _class_call(autoclass('android.provider.ContactsContract$Contacts'), args, instantiate)


def Phone(*args, instantiate: bool = False):
    return _class_call(
        autoclass('android.provider.ContactsContract$CommonDataKinds$Phone'),
        args, instantiate)
