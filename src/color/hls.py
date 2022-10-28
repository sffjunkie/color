import colorsys
from dataclasses import dataclass

from color.rgb import RGBColor


@dataclass(slots=True)
class HLSColor:
    hue: float = 0.0
    lightness: float = 0.0
    saturation: float = 0.0

    def from_rgb(self, color: RGBColor):
        self.hue, self.lightness, self.saturation = colorsys.rgb_to_hls(
            color.red, color.green, color.blue
        )

    def to_rgb(self) -> RGBColor:
        red, green, blue = colorsys.hls_to_rgb(
            self.hue, self.lightness, self.saturation
        )
        return RGBColor(red, green, blue)
