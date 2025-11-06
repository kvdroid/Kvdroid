from kvdroid.jclass.java import ByteBuffer


def bitmap_to_texture(bitmap):
    """
    Converts a bitmap object to a Kivy Texture instance.

    This function takes a bitmap image, extracts its pixel data, and creates a Texture
    that can be used within the Kivy framework for rendering graphics. The bitmap's
    pixel data is copied to a memory buffer, processed into a format suitable for
    Kivy texture creation, and returned as a texture object.

    :param bitmap: A bitmap object from which pixel data will be extracted. The bitmap
        should contain all necessary image data to facilitate the Texture object creation.
    :return: A Kivy Texture instance created from the provided bitmap.
    :rtype: Texture
    """

    from kivy.graphics.texture import Texture
    buffer = ByteBuffer().allocate(bitmap.getByteCount())
    bitmap.copyPixelsToBuffer(buffer)
    buffer_bytes = buffer.array().tostring()
    texture = Texture.create(size=(bitmap.getWidth(), bitmap.getHeight()), colorfmt='rgba')
    texture.blit_buffer(buffer_bytes, colorfmt='rgba', bufferfmt='ubyte')
    texture.flip_vertical()  # Flip the texture vertically to match Kivy's coordinate system
    return texture
