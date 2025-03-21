from random import randint
from typing import Callable

from jnius import JavaException

from kvdroid import activity
from kvdroid.jclass.android import Intent, Activity, VERSION_CODES, VERSION, SdkExtensions
from kvdroid.jclass.androidx import (
    PickVisualMedia,
    PickMultipleVisualMedia,
    PickVisualMediaImageOnly,
    PickVisualMediaRequestBuilder,
    PickVisualMediaVideoOnly,
    PickVisualMediaImageAndVideo,
    PickVisualMediaSingleMimeType
)
from kvdroid.jclass.android import MediaStore
from kvdroid.jinterface.activity import ActivityResultCallback
from android.runnable import run_on_ui_thread  # noqa
from android import activity as act  # noqa
from kvdroid.tools.uri import resolve_uri


def _register_picker(multiple: bool, callback):
    return activity.registerForActivityResult(
        PickMultipleVisualMedia(instantiate=True) if multiple else PickVisualMedia(instantiate=True),
        ActivityResultCallback(callback)
    )


@run_on_ui_thread
def pick_image_only(multiple: bool, callback):
    pick_media = _register_picker(multiple, callback)
    builder = PickVisualMediaRequestBuilder(instantiate=True)
    builder.setMediaType(PickVisualMediaImageOnly().INSTANCE)
    pick_media.launch(builder.build())


@run_on_ui_thread
def pick_video_only(multiple: bool, callback):
    pick_media = _register_picker(multiple, callback)
    builder = PickVisualMediaRequestBuilder(instantiate=True)
    builder.setMediaType(PickVisualMediaVideoOnly().INSTANCE)
    pick_media.launch(builder.build())


@run_on_ui_thread
def pick_image_and_video(multiple: bool, callback):
    pick_media = _register_picker(multiple, callback)
    builder = PickVisualMediaRequestBuilder(instantiate=True)
    builder.setMediaType(PickVisualMediaImageAndVideo().INSTANCE)
    pick_media.launch(builder.build())


@run_on_ui_thread
def pick_single_mimetype(multiple: bool, mimetype: str, callback):
    pick_media = _register_picker(multiple, callback)
    builder = PickVisualMediaRequestBuilder(instantiate=True)
    builder.setMediaType(PickVisualMediaSingleMimeType(mimetype))
    pick_media.launch(builder.build())


@run_on_ui_thread
def persist_background_permission(uri):
    flag = Intent().FLAG_GRANT_READ_URI_PERMISSION
    activity.context.contentResolver.takePersistableUriPermission(uri, flag)


_selection_single_code = None
_selection_multiple_code = None
_callback: Callable = lambda *_: None


def get_pick_images_max_limit():
    if VERSION().SDK_INT >= 33:
        return MediaStore().getPickImagesMaxLimit()
    if VERSION().SDK_INT >= 30:
        if SdkExtensions().getExtensionVersion(VERSION_CODES().R) >= 2:
            return MediaStore().getPickImagesMaxLimit()
    return 100


def is_photo_picker_available():
    if VERSION().SDK_INT >= 33:
        return True
    if VERSION().SDK_INT >= 30:
        if SdkExtensions().getExtensionVersion(VERSION_CODES().R) >= 2:
            return True
    return False


def action_pick_image(callback, pick_max=get_pick_images_max_limit(), multiple: bool = False):
    global _selection_single_code, _selection_multiple_code, _callback
    _selection_single_code = randint(12345, 654321)
    _selection_multiple_code = randint(654321, 754321)
    _callback = callback
    if is_photo_picker_available():
        intent = Intent(MediaStore().ACTION_PICK_IMAGES)
        if multiple:
            intent.putExtra(MediaStore().EXTRA_PICK_IMAGES_MAX, pick_max)
        activity.startActivityForResult(intent, _selection_multiple_code if multiple else _selection_single_code)
    else:
        raise JavaException(
            "Photo picker is not available on this android device. "
            "Possibly the android version is 10 or below or it's an Android Go device. "
            "Use 'chooser' instead from 'androidstorage4kivy' package"
        )


def _on_activity_result(request_code, result_code, data):
    if request_code not in (_selection_single_code, _selection_multiple_code):
        return

    if result_code != Activity().RESULT_OK:
        return

    if request_code == _selection_multiple_code:
        # Process multiple URI if multiple files selected
        selection = [
            resolve_uri(
                data.getClipData().getItemAt(count).getUri()
            ) for count in range(data.getClipData().getItemCount())
        ]
        _callback(selection)
    else:
        _callback(resolve_uri(data.getData()))


act.bind(on_activity_result=_on_activity_result)
