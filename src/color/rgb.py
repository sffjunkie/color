from dataclasses import dataclass

from typing_extensions import Self

from color import Color
from color.cie.xyz import (
    CIEXYZColor,
    RGBColorTransforms,
    TransformPair,
    xyz_normalized_primary_matrices,
)
from matrix import Matrix3x1


@dataclass(slots=True)
class RGBColor:
    red: float = 0.0
    green: float = 0.0
    blue: float = 0.0

    def to_xyz(self, color_space: str = "sRGB"):
        return rgb_to_xyz(self, color_space)

    @classmethod
    def from_xyz(cls, color: CIEXYZColor, color_space: str = "sRGB"):
        return cls(xyz_to_rgb_tuple(color, color_space))

    def to_ints(self):
        return (
            int(self.red * 255.0),
            int(self.green * 255.0),
            int(self.blue * 255.0),
        )

    @classmethod
    def from_ints(cls, *args: int):
        return cls(args[0] / 255.0, args[1] / 255.0, args[2] / 255.0)

    def intensity(self) -> float:
        return color_intensity(self)

    def contrast_color(self) -> Self:
        return contrast_color(self)


def rgb_to_xyz_tuple(color: RGBColor, color_space: str = "sRGB") -> CIEXYZColor:
    if color_space not in RGBColorTransforms:
        try:
            tf: TransformPair = xyz_normalized_primary_matrices(color_space)
            RGBColorTransforms[color_space] = tf
        except KeyError as exc:
            raise KeyError(f"Unknwon color space {color_space}") from exc

    transform = RGBColorTransforms[color_space].to_xyz

    rgb_m = Matrix3x1.from_iterable((color.red, color.green, color.blue))
    xyz_m = transform.multiply(rgb_m)
    return xyz_m.to_iterable()


def rgb_to_xyz(color: RGBColor, color_space: str = "sRGB") -> CIEXYZColor:
    return CIEXYZColor(rgb_to_xyz_tuple(color, color_space))


def xyz_to_rgb_tuple(color: CIEXYZColor, color_space: str = "sRGB") -> Color:
    if color_space not in RGBColorTransforms:
        try:
            tf: TransformPair = xyz_normalized_primary_matrices(color_space)
            RGBColorTransforms[color_space] = tf
        except KeyError as exc:
            raise KeyError(f"Unknwon color space {color_space}") from exc

    transform = RGBColorTransforms[color_space].to_rgb
    xyz_m = Matrix3x1((color.X, color.Y, color.Z))
    rgb_m = transform.multiply(xyz_m)
    return rgb_m.to_iterable()


def xyz_to_rgb(color: CIEXYZColor, color_space: str = "sRGB") -> RGBColor:
    return RGBColor(xyz_to_rgb_tuple(color, color_space))


def color_intensity(color: RGBColor) -> float:
    """Convert an RGB color to its intensity"""

    return color[0] * 0.299 + color[1] * 0.587 + color[2] * 0.114


def contrast_color(rgb: RGBColor) -> RGBColor:
    """Return either white or black whichever provides the most contrast"""

    if rgb == (0.0, 0.0, 0.0) or color_intensity(rgb) < (160.0 / 255.0):
        return (255.0, 255.0, 255.0)
    else:
        return (0.0, 0.0, 0.0)
