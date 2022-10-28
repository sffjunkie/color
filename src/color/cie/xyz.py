# Copyright 2014, Simon Kennedy, sffjunkie+code@gmail.com

"""Various functions to manipulate RGB hex, RGB, HSV and HLS colors."""

from dataclasses import dataclass
from typing import NamedTuple

from color.matrix import Matrix3x1, Matrix3x3

from . import Illuminants, RGBConversions, RGBReferencePrimaries

# RGB != CIERGB


@dataclass(slots=True)
class CIEXYZColor:
    X: float = 0.0
    Y: float = 0.0
    Z: float = 0.0


def w_matrix(illuminant: str) -> Matrix3x1:
    xy = Illuminants[illuminant]
    x = xy.x
    y = xy.y
    z = 1 - (x + y)

    return Matrix3x1.from_iterable([x / y, 1, z / y])


def p_matrix(primary: str) -> Matrix3x3:
    primaries = RGBReferencePrimaries[primary]
    data = [
        primaries["X"].red,
        primaries["X"].green,
        primaries["X"].blue,
        primaries["Y"].red,
        primaries["Y"].green,
        primaries["Y"].blue,
        primaries["Z"].red,
        primaries["Z"].green,
        primaries["Z"].blue,
    ]
    return Matrix3x3.from_iterable(data)


class TransformPair(NamedTuple):
    to_xyz: Matrix3x3
    to_rgb: Matrix3x3


def xyz_normalized_primary_matrices(
    color_space: str = "sRGB",
) -> tuple[Matrix3x3, Matrix3x3]:
    rgb_conversion = RGBConversions[color_space]
    w = w_matrix(rgb_conversion[0])
    p = p_matrix(rgb_conversion[1])
    coeffs = p.inverse() * w
    coeffs_diagonal_data = (
        coeffs[0],
        0.0,
        0.0,
        0.0,
        coeffs[1],
        0.0,
        0.0,
        0.0,
        coeffs[2],
    )
    coeffs_diagonal = Matrix3x3.from_iterable(coeffs_diagonal_data)
    npm = p * coeffs_diagonal
    return TransformPair(npm, npm.inverse())


RGBColorTransforms = {"sRGB": TransformPair(*xyz_normalized_primary_matrices("sRGB"))}
