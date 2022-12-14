from dataclasses import dataclass

from color import Color
from color.cie import Illuminants
from color.cie.xyz import CIEXYZColor

# References in brackets are from CIE 15:2004 3rd Edition

CUBE24_116 = (24.0 / 116.0) ** 3


@dataclass(slots=True)
class CIELABColor:
    L: float = 0.0
    a: float = 0.0
    b: float = 0.0

    def to_xyz(self, illuminant: str = "D65"):
        return lab_to_xyz(self, illuminant)

    @classmethod
    def from_xyz(cls, color: CIEXYZColor, illuminant: str = "D65"):
        return cls(*xyz_to_lab_tuple(color, illuminant))


def lab_to_xyz_tuple(color: CIELABColor, illuminant: str = "D65") -> Color:
    i = Illuminants[illuminant]
    Xn = i.x
    Yn = i.y
    Zn = 1 - Xn - Yn

    Xn = Xn / Yn
    Zn = Zn / Yn
    Yn = 1

    l_star = color.L
    a_star = color.a
    b_star = color.b

    fY = (l_star + 16.0) / 116.0  # (D.1)
    fX = (a_star / 500.0) + fY  # (D.2)
    fZ = fY - (b_star / 200.0)  # (D.3)

    def f(t: float, l_star: float = -1) -> float:
        if t > 24.0 / 116.0 or l_star > 8.0:
            return t**3  # (D.4, D.6, D.7)
        else:
            return (t - (16.0 / 116.0)) * (108.0 / 841.0)  # (D.5, D.7, D.9)

    X = Xn * f(fX)
    Y = Yn * f(fY, l_star)
    Z = Zn * f(fZ)

    return X, Y, Z


def lab_to_xyz(color: CIELABColor, illuminant: str = "D65") -> CIEXYZColor:
    return CIEXYZColor(*lab_to_xyz_tuple(color, illuminant))


def xyz_to_lab_tuple(color: CIEXYZColor, illuminant: str = "D65") -> Color:
    i = Illuminants[illuminant]
    Xn = i.x
    Yn = i.y
    Zn = 1 - Xn - Yn

    Xn = Xn / Yn
    Zn = Zn / Yn
    Yn = 1

    X = color.X
    Y = color.Y
    Z = color.Z

    def f(t: float) -> float:
        if t > CUBE24_116:
            return t ** (1.0 / 3.0)  # (8.6, 8.8, 8.10)
        else:
            return ((841 / 108) * t + 16) / 116  # (8.7, 8.9, 8.11)

    y = f(Y / Yn)
    x = f(X / Xn)
    z = f(Z / Zn)

    Lstar = 116 * y - 16.0  # L* (8.3) y=0.1107
    Astar = 500 * (x - y)  # a* (8.4)
    Bstar = 200 * (y - z)  # b* (8.5)

    return Lstar, Astar, Bstar


def xyz_to_lab(color: CIEXYZColor, illuminant: str = "D65") -> CIELABColor:
    return CIELABColor(*xyz_to_lab_tuple(color, illuminant))
