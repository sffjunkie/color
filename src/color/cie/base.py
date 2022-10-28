from typing import NamedTuple


class UVChromaticity(NamedTuple):
    u: float
    v: float


class XYChromaticity(NamedTuple):
    x: float
    y: float

    @classmethod
    def from_uv(cls, uv: UVChromaticity):
        denom = 12 + 6 * uv.u - 16 * uv.v
        x = 9 * uv.u / denom
        y = 4 * uv.v / denom
        return cls(x, y)

    @property
    def z(self):
        return 1.0 - self.x - self.y


Illuminants = {
    # D = Daylight, Color Temperature = Number * 100
    "D65": XYChromaticity(0.31271, 0.32902),
    "D55": XYChromaticity(0.3324, 0.3474),
    "D50": XYChromaticity(0.3457, 0.3585),
    "IIIC": XYChromaticity(0.3101, 0.3162),
}


class RGBPrimary(NamedTuple):
    red: float
    green: float
    blue: float


RGBReferencePrimaries = {
    "REC709": {
        "X": RGBPrimary(0.64, 0.30, 0.15),
        "Y": RGBPrimary(0.33, 0.60, 0.06),
        "Z": RGBPrimary(1 - (0.64 + 0.33), 1 - (0.30 + 0.60), 1 - (0.15 + 0.06)),
    },
    "sRGB": {
        "X": RGBPrimary(0.64, 0.30, 0.15),
        "Y": RGBPrimary(0.33, 0.60, 0.06),
        "Z": RGBPrimary(1 - (0.64 + 0.33), 1 - (0.30 + 0.60), 1 - (0.15 + 0.06)),
    },
}

RGBConversions = {
    "REC709": ("D65", "REC709"),
    "sRGB": ("D65", "sRGB"),
}


__all__ = [
    "UVChromaticity",
    "XYChromaticity",
    "Illuminants",
    "RGBPrimary",
    "RGBReferencePrimaries",
    "RGBConversions",
]
