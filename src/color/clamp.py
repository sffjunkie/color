from color import Color


def clamp_value(value: float) -> float:
    """Clamp a float between 0.0 and 1.0"""

    return min(max(0.0, float(value)), 1.0)


def color_clamped(value: Color):
    """Clamps the values in a tuple between 0.0 and 1.0"""
    return tuple([clamp_value(elem) for elem in value])
