from kvdroid.cast import cast_object
from kvdroid.jclass.android import Bitmap, CompressFormat, Config, Canvas, AdaptiveIconDrawable
from kvdroid.jclass.java import FileOutputStream


def save_drawable(drawable, path, name):
    if isinstance(drawable, AdaptiveIconDrawable()):
        drawable = cast_object("adaptiveicondrawable", drawable)
    else:
        drawable = cast_object("bitmapdrawable", drawable)

    height = drawable.getIntrinsicHeight() if drawable.getIntrinsicHeight() > 0 else 1
    width = drawable.getIntrinsicWidth() if drawable.getIntrinsicWidth() > 0 else 1
    if drawable.isFilterBitmap():
        bitmap = drawable.getBitmap()
    else:
        bitmap = Bitmap().createBitmap(width, height, Config().ARGB_8888)
        canvas = Canvas(bitmap)
        drawable.setBounds(0, 0, canvas.getWidth(), canvas.getHeight())
        drawable.draw(canvas)
    out = FileOutputStream(path+name+".png")
    bitmap.compress(CompressFormat().PNG, 90, out)
    return path + name + ".png"
  
