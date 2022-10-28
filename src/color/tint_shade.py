from color import Color
from color.clamp import clamp_value
from color.rgb import RGBColor


def luminosity_transform(color: Color, luminosity=0.05):
    """Transform an RGB color by a luminosity.

    If luminosity is a tuple then the 3 elements are used to transform the red,
    green and blue values individually. If a float then the same value is used
    to transform all 3 elements."""

    if isinstance(luminosity, tuple):
        luminosity = luminosity[:3]
    else:
        luminosity = (luminosity, luminosity, luminosity)

    return tuple([clamp_value(e + l) for e, l in zip(color, luminosity)])


def rgb_tint(rgb: RGBColor, percent: float = 5):
    """Create a tinted version of the RGB color

    :param rgb: The RGB value for which to calculate the tint
    :type rgb:  tuple
    :param percent: Determines the percent between the specified color and
                     the tint
    :type percent:  int
    """
    return luminosity_transform(rgb, percent / 100)


def rgb_tints(rgb: RGBColor, base_percent: float, count: int, linear: bool = True):
    """Produce a list of tints from the base color

    :param rgb: The RGB value for which to calculate the tints
    :type rgb:  tuple
    :param base_percent: Determines the factor between the returned colors
    :type base_percent:  float
    :param count: The number of tints to return
    :type count: int
    """
    factor = base_percent
    tints = []
    number_to_calc = (2 * count) - 1
    for _ in range(number_to_calc):
        if factor < 100:
            tints.append(rgb_tint(rgb, factor))
        else:
            tints.append(None)

        if linear:
            factor += base_percent
        else:
            factor *= 1.0 + (base_percent / 100.0)

    # Remove any duplicates from the end
    for _ in range(number_to_calc - 1):
        t1 = tints[-1]
        t2 = tints[-2]

        if not t1:
            tints.pop()
        elif t1 and t2:
            if (
                int(t1[0] * 255) == int(t2[0] * 255)
                and int(t1[1] * 255) == int(t2[1] * 255)
                and int(t1[2] * 255) == int(t2[2] * 255)
            ):

                tints.pop()
            else:
                break

    tints = tints[:count]
    # tints.reverse()
    return tints


def rgb_shade(rgb, percent=5):
    """Create a shade of the RGB color

    :param rgb: The RGB value for which to calculate the tint
    :type rgb:  tuple
    :param percent: Determines the percent between the specified color and
                    the shade
    :type percent:  int
    """
    return luminosity_transform(rgb, -percent / 100)


def rgb_shades(rgb: RGBColor, base_percent: float, count: int, linear: bool = True):
    """Produce a list of shades from the base color

    :param rgb: The RGB value for which to calculate the shades
    :type rgb:  tuple
    :param base_percent: Determines the factor between the returned colors
    :type base_percent:  float
    :param count: The number of shades to return
    :type count:  int
    """
    factor = base_percent
    shades = []
    number_to_calc = (2 * count) - 1
    for dummy in range(number_to_calc):
        if factor < 100:
            shades.append(rgb_shade(rgb, factor))
        else:
            shades.append(None)

        if linear:
            factor += base_percent
        else:
            factor *= 1.0 - (base_percent / 100.0)

    # Remove any duplicates from the end
    for dummy in range(number_to_calc - 1):
        s1 = shades[-1]
        s2 = shades[-2]

        if not s1:
            shades.pop()
        elif s1 and s2:
            if (
                int(s1[0] * 255) == int(s2[0] * 255)
                and int(s1[1] * 255) == int(s2[1] * 255)
                and int(s1[2] * 255) == int(s2[2] * 255)
            ):

                shades.pop()
            else:
                break

    return shades[:count]
