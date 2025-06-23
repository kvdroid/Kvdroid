from jnius import autoclass
from kvdroid.jclass import _class_call


def Settings(*args, instantiate: bool = False):
    return _class_call(autoclass('android.provider.Settings'), args, instantiate)


def Contacts(*args, instantiate: bool = False):
    return _class_call(autoclass('android.provider.ContactsContract$Contacts'), args, instantiate)


def DocumentsContract(*args, instantiate: bool = False):
    return _class_call(autoclass('android.provider.DocumentsContract'), args, instantiate)


def Phone(*args, instantiate: bool = False):
    return _class_call(
        autoclass('android.provider.ContactsContract$CommonDataKinds$Phone'),
        args, instantiate)


def MediaStore(*args, instantiate: bool = False):
    return _class_call(autoclass("android.provider.MediaStore"), args, instantiate)


def MediaStoreFiles(*args, instantiate: bool = False):
    return _class_call(autoclass('android.provider.MediaStore$Files'), args, instantiate)


def MediaStoreAudioMedia(*args, instantiate: bool = False):
    return _class_call(autoclass('android.provider.MediaStore$Audio$Media'), args, instantiate)


def MediaStoreAudioCoulmns(*args, instantiate: bool = False):
    return _class_call(autoclass('android.provider.MediaStore$Audio$AudioColumns'), args, instantiate)


def MediaStoreAudioAlbumColumns(*args, instantiate: bool = False):
    return _class_call(autoclass('android.provider.MediaStore$Audio$AlbumColumns'), args, instantiate)


def MediaStoreImagesMedia(*args, instantiate: bool = False):
    return _class_call(autoclass('android.provider.MediaStore$Images$Media'), args, instantiate)


def MediaStoreVideoMedia(*args, instantiate: bool = False):
    return _class_call(autoclass('android.provider.MediaStore$Video$Media'), args, instantiate)


def MediaStoreDownloads(*args, instantiate: bool = False):
    return _class_call(autoclass('android.provider.MediaStore$Downloads'), args, instantiate)


def MediaStoreMediaColumns(*args, instantiate: bool = False):
    return _class_call(autoclass('android.provider.MediaStore$MediaColumns'), args, instantiate)


def TelephonySms(*args, instantiate: bool = False):
    return _class_call(autoclass('android.provider.Telephony$Sms'), args, instantiate)


def CallLogCalls(*args, instantiate: bool = False):
    return _class_call(autoclass('android.provider.CallLog$Calls'), args, instantiate)
