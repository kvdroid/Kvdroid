from typing import Union

from kvdroid.cast import cast_object
from kvdroid.jclass.android import (
    Bitmap,
    BitmapCompressFormat,
    BitmapConfig,
    Canvas,
    AdaptiveIconDrawable,
    BitmapDrawable,
)
from kvdroid.jclass.androidx.core.content.res import ResourcesCompat
from kvdroid.jclass.java import FileOutputStream
from kvdroid import activity
from kvdroid.jclass.android import BitmapFactory

BitmapFactory = BitmapFactory()


def save_drawable(drawable, path, name):
    if isinstance(drawable, AdaptiveIconDrawable()):
        drawable = cast_object("adaptiveIconDrawable", drawable)
    else:
        drawable = cast_object("bitmapDrawable", drawable)

    height = drawable.getIntrinsicHeight() if drawable.getIntrinsicHeight() > 0 else 1
    width = drawable.getIntrinsicWidth() if drawable.getIntrinsicWidth() > 0 else 1
    if drawable.isFilterBitmap():
        bitmap = drawable.getBitmap()
    else:
        bitmap = Bitmap().createBitmap(width, height, BitmapConfig().ARGB_8888)
        canvas = Canvas(bitmap)
        drawable.setBounds(0, 0, canvas.getWidth(), canvas.getHeight())
        drawable.draw(canvas)
    out = FileOutputStream(path + name + ".png")
    bitmap.compress(BitmapCompressFormat().PNG, 90, out)
    return path + name + ".png"


def get_bitmap(image: int | str | object):  # object must be a java InputStream
    if isinstance(image, int):
        bitmap = BitmapFactory.decodeResource(activity.getResources(), image)
    elif isinstance(image, str):
        bitmap = BitmapFactory.decodeFile(image)
    else:
        bitmap = BitmapFactory.decodeStream(image)
    return bitmap


def bitmap_to_drawable(bitmap):
    return BitmapDrawable(activity.getResources(), bitmap)


def get_drawable(resource_id):
    res = activity.getResources()
    return ResourcesCompat().getDrawable(res, resource_id, None)


def compress_image(path_or_bitmap, quality=100, compress_format="jpeg"):
    if isinstance(path_or_bitmap, str):
        bitmap = get_bitmap(path_or_bitmap)
    else:
        bitmap = path_or_bitmap
    baos = ByteArrayOutputStream(instantiate=True)
    if compress_format == "jpeg":
        bitmap.compress(BitmapCompressFormat().JPEG, quality, baos)
    else:
        bitmap.compress(BitmapCompressFormat().PNG, quality, baos)
    byte_array = baos.toByteArray()
    return byte_array, BitmapFactory().decodeByteArray(byte_array, 0, len(byte_array))


def create_scaled_bitmap(path_or_bitmap, target_size):
    if isinstance(path_or_bitmap, str):
        bitmap = get_bitmap(path_or_bitmap)
    else:
        bitmap = path_or_bitmap

    width = bitmap.getWidth()
    height = bitmap.getHeight()

    if width <= target_size >= height:
        return bitmap

    scale = target_size / max(height, width)
    new_width = width * scale
    new_height = height * scale

    return Bitmap().createScaledBitmap(bitmap, new_width, new_height, True)