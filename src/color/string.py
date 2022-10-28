import colorsys
import string

from color.rgb import RGBColor


def rgbcolor_to_rgb_hex(value: RGBColor) -> str:
    """Convert from an (R, G, B) tuple to a hex color.

    :param value: The RGB value to convert

    R, G and B should be in the range 0.0 - 1.0
    """
    color = "".join(["%02x" % x1 for x1 in [int(x * 255) for x in value]])
    return "#%s" % color


def rgbcolor_to_rgb_string(value: RGBColor, dp: int = 3) -> str:
    """Convert from an (R, G, B) tuple to an RGB string `rgb(red,green,blue)`.

    :param value: The RGB value to convert
    :param dp: Number of decimal places in the string

    R, G and B should be in the range 0.0 - 1.0
    """
    format_str = "%%.0%df" % dp
    value = "rgb(%s)" % (",".join([format_str % x for x in value]))
    return value


def rgbcolor_to_hsv_string(value: RGBColor, dp: int = 3) -> str:
    """Convert from an (R, G, B) tuple to an HSV string.

    :param value: The RGB value to convert
    :param dp: Number of decimal places in the string

    R, G and B should be in the range 0.0 - 1.0
    """
    hsv = colorsys.rgb_to_hsv(*value)
    format_str = "%%.0%df" % dp
    hsv = "hsv(%s)" % (",".join([format_str % x for x in hsv]))
    return hsv


def rgbcolor_to_hls_string(value: RGBColor, dp: int = 3):
    """Convert from an (R, G, B) tuple to an HLS string.

    :param value: The RGB value to convert
    :param dp: Number of decimal places in the string

    R, G and B should be in the range 0.0 - 1.0
    """
    hls = colorsys.rgb_to_hls(*value)
    format_str = "%%.0%df" % dp
    hls = "hls(%s)" % (",".join([format_str % x for x in hls]))
    return hls


def hex_string_to_rgbcolor(value: str, allow_short: bool = True) -> RGBColor:
    """Convert from a hex color string of the form `#abc` or `#abcdef` to an
    RGB tuple.

    :param value: The value to convert
    :param allow_short: If True then the short of form of an hex value is
                        accepted e.g. #fff
    """
    if value[0] != "#":
        return None

    for ch in value[1:]:
        if ch not in string.hexdigits:
            return None

    if len(value) == 7:
        # The following to_iterable function is based on the
        # :func:`grouper` function in the Python standard library docs
        # http://docs.python.org/library/itertools.html
        def to_iterable():
            args = [iter(value[1:])] * 2
            return tuple([int("%s%s" % t, 16) / 255 for t in zip(*args)])

    elif len(value) == 4 and allow_short:

        def to_iterable():
            return tuple([int("%s%s" % (t, t), 16) / 255 for t in value[1:]])

    else:
        return None

    try:
        return to_iterable()
    except ValueError:
        return None
