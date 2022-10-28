import colorsys
from dataclasses import dataclass

from color.rgb import RGBColor


@dataclass(slots=True)
class HSVColor:
    hue: float = 0.0
    saturation: float = 0.0
    value: float = 0.0

    def from_rgb(self, color: RGBColor):
        self.hue, self.saturation, self.value = colorsys.rgb_to_hsv(
            color.red, color.green, color.blue
        )

    def to_rgb(self) -> RGBColor:
        red, green, blue = colorsys.hsv_to_rgb(self.hue, self.saturation, self.value)
        return RGBColor(red, green, blue)
