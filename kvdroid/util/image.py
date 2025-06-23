import struct


def get_jpeg_size_from_bytes(image_bytes):
    """
    Extracts JPEG image dimensions (width, height) from its byte data.
    Pure Python, no external libraries.
    """
    # JPEG magic number: FF D8 (SOI - Start Of Image)
    if not image_bytes.startswith(b'\xFF\xD8'):
        return None, None  # Not a JPEG

    offset = 2  # Skip SOI (FF D8)
    while offset < len(image_bytes):
        marker = image_bytes[offset:offset + 2]

        # Check for marker FFXX (excluding FF00-FF7F which are data, and FFD0-FFD7 RSTn)
        if marker[0] == 0xFF and 0xC0 <= marker[1] <= 0xCF and marker[1] not in [0xC4, 0xC8, 0xCC]:  # SOF markers
            # Found an SOF marker (e.g., FFC0, FFC1, FFC2, etc.)
            length = struct.unpack('>H', image_bytes[offset + 2:offset + 4])[0]

            if offset + 4 + 5 > len(image_bytes):  # 4 bytes for marker+length, 5 for precision+height+width
                return None, None  # Incomplete header

            # The SOF segment structure (after marker and length):
            # 1 byte: Sample precision (bits per component, usually 8)
            # 2 bytes: Height (big-endian)
            # 2 bytes: Width (big-endian)
            height = struct.unpack('>H', image_bytes[offset + 5:offset + 7])[0]
            width = struct.unpack('>H', image_bytes[offset + 7:offset + 9])[0]
            return width, height

        elif marker[0] == 0xFF and 0xD0 <= marker[1] <= 0xD9:  # Restart markers FFD0-FFD7, EOI FFD9
            # Skip these, they don't have lengths
            offset += 2
        elif marker == b'\xFF\xDA':  # SOS (Start Of Scan) - image data follows
            return None, None  # Dimensions not found before image data
        elif marker[0] == 0xFF:  # Other markers (APP segments, COM, DQT, DHT, DRI, etc.)
            if offset + 4 > len(image_bytes):
                return None, None  # Incomplete segment length
            length = struct.unpack('>H', image_bytes[offset + 2:offset + 4])[0]
            offset += 2 + length  # Marker (2 bytes) + Length (2 bytes) + Data (length-2 bytes)
        else:  # Not a valid marker, likely corrupt or unexpected data
            return None, None  # Invalid JPEG structure

    return None, None  # SOF marker not found


def get_png_size_from_bytes(image_bytes):
    """
    Extracts PNG image dimensions (width, height) from its byte data.
    Pure Python, no external libraries.
    """
    # PNG magic number: 89 50 4E 47 0D 0A 1A 0A
    if not image_bytes.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
        return None, None  # Not a PNG

    # IHDR chunk starts after the 8-byte signature.
    # Check if we have enough bytes for the IHDR chunk header + data (8 signature + 4 length + 4 type + 13 data)
    if len(image_bytes) < 8 + 4 + 4 + 13:
        return None, None  # Not enough bytes for full IHDR

    # Check that it's actually an IHDR chunk at the expected position
    chunk_type = image_bytes[12:16]
    if chunk_type != b'IHDR':
        return None, None  # Malformed PNG, IHDR not in expected place

    # Extract width and height from bytes 16-24 (after signature, length, type)
    width, height = struct.unpack('>II', image_bytes[16:24])
    return width, height


def get_gif_size_from_bytes(image_bytes):
    """
    Extracts GIF image dimensions (width, height) from its byte data.
    Pure Python, no external libraries.
    """
    # GIF magic number: GIF87a or GIF89a
    if not (image_bytes.startswith(b'GIF87a') or image_bytes.startswith(b'GIF89a')):
        return None, None  # Not a GIF

    # The Logical Screen Descriptor starts at byte 6.
    # Check if we have enough bytes for the signature + width/height (6 + 2 + 2)
    if len(image_bytes) < 10:
        return None, None  # Not enough bytes for size information

    # Extract width and height from bytes 6-10 (little-endian)
    width, height = struct.unpack('<HH', image_bytes[6:10])
    return width, height


def get_bmp_size_from_bytes(image_bytes):
    """
    Extracts BMP image dimensions (width, height) from its byte data.
    Pure Python, no external libraries.
    """
    # BMP magic number: 'BM'
    if not image_bytes.startswith(b'BM'):
        return None, None  # Not a BMP

    # BMP headers can vary in size.
    # The DIB header starts at offset 14 (after the 14-byte File Header).
    # The DIB header length (4 bytes) is at offset 14.
    # For BITMAPINFOHEADER (40 bytes), which is common:
    # Width is at offset 18 (4 bytes, signed integer)
    # Height is at offset 22 (4 bytes, signed integer)

    if len(image_bytes) < 26:  # Need at least up to height field
        return None, None  # Not enough bytes

    dib_header_size = struct.unpack('<I', image_bytes[14:18])[0]

    if dib_header_size >= 40:  # BITMAPINFOHEADER or larger
        width = struct.unpack('<i', image_bytes[18:22])[0]
        height = struct.unpack('<i', image_bytes[22:26])[0]
        # Height can be negative for top-down DIBs; take absolute value for display size
        return abs(width), abs(height)
    elif dib_header_size == 12:  # BITMAPCOREHEADER (older, less common)
        # Width at 18 (2 bytes), Height at 20 (2 bytes)
        if len(image_bytes) < 22:
            return None, None
        width, height = struct.unpack('<HH', image_bytes[18:22])
        return width, height

    return None, None  # Unsupported BMP header type or insufficient data


def get_tiff_size_from_bytes(image_bytes):
    """
    Extracts TIFF image dimensions (width, height) from its byte data.
    Pure Python, no external libraries.
    TIFF is complex due to IFDs and different byte orders. This is a basic attempt.
    """
    if len(image_bytes) < 8:
        return None, None

    # Byte order: 'II' (little-endian) or 'MM' (big-endian)
    byte_order_marker = image_bytes[0:2]
    if byte_order_marker == b'II':  # Intel byte order (little-endian)
        endian_char = '<'
    elif byte_order_marker == b'MM':  # Motorola byte order (big-endian)
        endian_char = '>'
    else:
        return None, None  # Not a TIFF

    # Check TIFF magic number (42) at offset 2
    if struct.unpack(endian_char + 'H', image_bytes[2:4])[0] != 42:
        return None, None

    # Offset to the first Image File Directory (IFD)
    first_ifd_offset = struct.unpack(endian_char + 'I', image_bytes[4:8])[0]

    # IFD starts with the number of directory entries (2 bytes)
    if len(image_bytes) < first_ifd_offset + 2:
        return None, None
    num_entries = struct.unpack(endian_char + 'H', image_bytes[first_ifd_offset:first_ifd_offset + 2])[0]

    # Each IFD entry is 12 bytes long
    # Structure of an IFD entry:
    # 2 bytes: Tag (e.g., 256 for ImageWidth, 257 for ImageLength)
    # 2 bytes: Type (e.g., 3 for SHORT, 4 for LONG)
    # 4 bytes: Count
    # 4 bytes: Value Offset (or actual value if it fits in 4 bytes)

    width = None
    height = None

    for i in range(num_entries):
        entry_offset = first_ifd_offset + 2 + (i * 12)
        if len(image_bytes) < entry_offset + 12:
            break  # Not enough bytes for this entry

        tag, type_code, count, value_offset = struct.unpack(endian_char + 'HHII',
                                                            image_bytes[entry_offset:entry_offset + 12])

        # Tag 256: ImageWidth
        if tag == 256:
            if type_code == 3:  # SHORT (2 bytes)
                width = struct.unpack(endian_char + 'H', image_bytes[entry_offset + 8:entry_offset + 10])[0]
            elif type_code == 4:  # LONG (4 bytes)
                width = value_offset  # Value fits in 4 bytes
            # For other types (e.g., 5 for RATIONAL), more complex parsing is needed.
        # Tag 257: ImageLength (Height)
        elif tag == 257:
            if type_code == 3:  # SHORT (2 bytes)
                height = struct.unpack(endian_char + 'H', image_bytes[entry_offset + 8:entry_offset + 10])[0]
            elif type_code == 4:  # LONG (4 bytes)
                height = value_offset  # Value fits in 4 bytes

        if width is not None and height is not None:
            return width, height

    return None, None


# Main dispatcher function
def get_image_size_from_bytes(image_bytes):
    """
    Attempts to determine the width and height of an image from its byte data
    by trying different image format parsers.
    Returns (width, height) or (None, None) if type not recognized or size not found.
    """
    parsers = [
        get_jpeg_size_from_bytes,
        get_png_size_from_bytes,
        get_gif_size_from_bytes,
        get_bmp_size_from_bytes,
        get_tiff_size_from_bytes,  # TIFF is complex and this is a basic implementation
        # Add more parsers here for other formats (WebP, ICO, etc.)
    ]

    for parser in parsers:
        width, height = parser(image_bytes)
        if width is not None and height is not None:
            return width, height

    return None, None


# --- Example Usage ---

# Function to load image bytes (for testing)
def load_image_bytes(filepath):
    try:
        with open(filepath, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"An error occurred loading {filepath}: {e}")
        return None


if __name__ == "__main__":
    # Create dummy files for testing (these are NOT valid, complete images,
    # but their headers contain the info for this parser to work)

    # Dummy JPEG (minimal, just enough to find SOF0 marker)
    # A tiny (invalid) JPEG header that points to width=100, height=50
    dummy_jpeg_bytes = (
        b'\xFF\xD8'  # SOI
        b'\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'  # APP0 (JFIF)
        b'\xFF\xC0\x00\x11\x08\x00\x32\x00\x64\x03\x01\x22\x00\x02\x11\x01\x03\x11\x01'  # SOF0: height=50, width=100
        b'\xFF\xDA'  # SOS (Start of Scan) - actual image data would follow
    )
    with open("dummy.jpg", "wb") as f:
        f.write(dummy_jpeg_bytes)

    # Dummy PNG
    dummy_png_bytes = (
        b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'  # PNG signature
        b'\x00\x00\x00\x0D'  # IHDR chunk length (13 bytes)
        b'IHDR'  # IHDR chunk type
        b'\x00\x00\x00\xC8'  # Width: 200 (big-endian)
        b'\x00\x00\x00\x78'  # Height: 120 (big-endian)
        b'\x08\x06\x00\x00\x00'  # Bit depth=8, color type=RGB+Alpha (6), etc. (5 more bytes)
    )
    with open("dummy.png", "wb") as f:
        f.write(dummy_png_bytes)

    # Dummy GIF
    dummy_gif_bytes = (
        b'GIF89a'  # GIF signature
        b'\x40\x01'  # Width: 320 (0x0140 little-endian)
        b'\xE0\x00'  # Height: 224 (0x00E0 little-endian)
        b'\x91\x00\x00'  # Packed field, Background color index, Pixel Aspect Ratio
    )
    with open("dummy.gif", "wb") as f:
        f.write(dummy_gif_bytes)

    # Dummy BMP (BITMAPINFOHEADER type, common)
    # Width=256, Height=192
    dummy_bmp_bytes = (
        b'BM'  # Signature
        b'\x00\x00\x00\x00'  # File size (placeholder)
        b'\x00\x00\x00\x00'  # Reserved
        b'\x36\x00\x00\x00'  # Offset to pixel data (54 bytes for common header)
        b'\x28\x00\x00\x00'  # DIB Header Size (40 bytes for BITMAPINFOHEADER)
        b'\x00\x01\x00\x00'  # Width: 256 (little-endian)
        b'\xC0\x00\x00\x00'  # Height: 192 (little-endian)
        b'\x01\x00'  # Planes (1)
        b'\x18\x00'  # Bits per pixel (24)
        b'\x00\x00\x00\x00'  # Compression method (0 for BI_RGB)
        b'\x00\x00\x00\x00'  # Image size (placeholder)
        b'\x00\x00\x00\x00'  # X-pixels per meter
        b'\x00\x00\x00\x00'  # Y-pixels per meter
        b'\x00\x00\x00\x00'  # Colors in color table
        b'\x00\x00\x00\x00'  # Important color count
    )
    with open("dummy.bmp", "wb") as f:
        f.write(dummy_bmp_bytes)

    # Dummy TIFF (little-endian for simplicity, width=300, height=200)
    # This is a very simplified TIFF header
    dummy_tiff_bytes = (
        b'II'  # Byte order: Little-endian
        b'\x2A\x00'  # Magic number (42)
        b'\x08\x00\x00\x00'  # Offset to first IFD (8 bytes)

        # IFD starts here (at offset 8)
        b'\x02\x00'  # Number of entries in IFD: 2

        # Entry 1: ImageWidth (Tag 256, Type SHORT)
        b'\x00\x01'  # Tag: 256 (0x0100)
        b'\x03\x00'  # Type: 3 (SHORT)
        b'\x01\x00\x00\x00'  # Count: 1
        b'\x2C\x01\x00\x00'  # Value: 300 (0x012C) - fits in 4 bytes

        # Entry 2: ImageLength (Tag 257, Type SHORT)
        b'\x01\x01'  # Tag: 257 (0x0101)
        b'\x03\x00'  # Type: 3 (SHORT)
        b'\x01\x00\x00\x00'  # Count: 1
        b'\xC8\x00\x00\x00'  # Value: 200 (0x00C8) - fits in 4 bytes

        b'\x00\x00\x00\x00'  # Next IFD offset (0 for none)
    )
    with open("dummy.tif", "wb") as f:
        f.write(dummy_tiff_bytes)

    # Test cases
    files_to_test = {
        "dummy.jpg": "JPEG",
        "dummy.png": "PNG",
        "dummy.gif": "GIF",
        "dummy.bmp": "BMP",
        "dummy.tif": "TIFF",
        "non_existent.xyz": "Unknown"  # Test for file not found
    }

    for filename, filetype in files_to_test.items():
        print(f"\n--- Testing {filename} ({filetype}) ---")
        image_data = load_image_bytes(filename)
        if image_data:
            width, height = get_image_size_from_bytes(image_data)
            if width is not None and height is not None:
                print(f"Detected size: {width}x{height}")
            else:
                print(
                    f"Could not determine size for {filename}. Image type might not be supported or file is malformed.")
        else:
            print(f"Could not load data for {filename}.")

    # Clean up dummy files
    import os

    for filename in files_to_test.keys():
        if os.path.exists(filename):
            os.remove(filename)