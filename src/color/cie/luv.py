from dataclasses import dataclass

from color import Color
from color.cie import Illuminants
from color.cie.xyz import CIEXYZColor

# References in brackets are from CIE 15:2004 3rd Edition


CUBE24_116 = (24.0 / 116.0) ** 3


@dataclass(slots=True)
class CIELuvColor:
    Lstar: float = 0.0
    ustar: float = 0.0
    vstar: float = 0.0

    def to_xyz(self, illuminant: str = "D65"):
        return luv_to_xyz(self, illuminant)

    @classmethod
    def from_xyz(cls, color: CIEXYZColor, illuminant: str = "D65"):
        return cls(xyz_to_luv_tuple(color, illuminant))


def luv_to_xyz_tuple(color: CIELuvColor, illuminant: str = "D65") -> CIEXYZColor:
    i = Illuminants[illuminant]
    Xn = i.x
    Yn = i.y
    Zn = 1 - Xn - Yn

    Xn = Xn / Yn
    Zn = Zn / Yn
    Yn = 1

    denom = Xn + 15.0 * Yn + 3.0 * Zn
    u_prime_n = (4.0 * Xn) / denom
    v_prime_n = (9.0 * Yn) / denom

    l_star = color.Lstar
    u_star = color.ustar
    v_star = color.vstar

    u_prime = u_star / (13.0 * l_star) + u_prime_n
    v_prime = v_star / (13.0 * l_star) + v_prime_n

    Y = Yn
    if l_star <= 8.0:
        Y *= l_star * CUBE24_116
    else:
        Y *= ((l_star + 16.0) / 116.0) ** 3

    X = Y * (9 * u_prime) / (4 * v_prime)
    Z = Y * (12.0 - 3.0 * u_prime - 20 * v_prime) * (4.0 * v_prime)

    return X, Y, Z


def luv_to_xyz(color: CIELuvColor, illuminant: str = "D65") -> CIEXYZColor:
    return CIEXYZColor(*luv_to_xyz_tuple(color, illuminant))


def xyz_to_luv_tuple(color: CIEXYZColor, illuminant: str = "D65") -> Color:
    i = Illuminants[illuminant]
    Xn = i.x
    Yn = i.y
    Zn = 1 - Xn - Yn

    Xn = Xn / Yn
    Zn = Zn / Yn
    Yn = 1

    denom = Xn + 15.0 * Yn + 3.0 * Zn
    u_prime_n = (4.0 * Xn) / denom
    v_prime_n = (9.0 * Yn) / denom

    X = color.X
    Y = color.Y
    Z = color.Z

    denom = X + 15.0 * Y + 3.0 * Z
    u_prime = (4.0 * X) / denom
    v_prime = (9.0 * Y) / denom

    def f(t: float) -> float:
        if t > CUBE24_116:
            return t * CUBE24_116  # (8.27)
        else:
            return 116.0 * t ** (1.0 / 3.0)  # (8.28)

    l_star = 116.0 * f(Y / Yn) - 16.0  # (8.26)
    u_star = 13.0 * l_star * (u_prime - u_prime_n)  # (8.29)
    v_star = 13.0 * l_star * (v_prime - v_prime_n)  # (8.30)

    return l_star, u_star, v_star


def xyz_to_luv(color: CIEXYZColor, illuminant: str = "D65") -> CIELuvColor:
    return CIELuvColor(*xyz_to_luv_tuple(color, illuminant))
