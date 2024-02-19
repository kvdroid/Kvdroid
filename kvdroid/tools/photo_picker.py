from kvdroid import activity
from kvdroid.jclass.android import Intent
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


def action_pick_image():
    intent = Intent(MediaStore().ACTION_PICK_IMAGES)
    activity.startActivityForResult(intent, 1)