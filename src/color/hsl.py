import colorsys
from dataclasses import dataclass

from color.rgb import RGBColor


@dataclass(slots=True)
class HSLColor:
    hue: float = 0.0
    saturation: float = 0.0
    lightness: float = 0.0

    @classmethod
    def from_rgb(cls, color: RGBColor):
        hue, lightness, saturation = colorsys.rgb_to_hls(
            color.red, color.green, color.blue
        )
        return cls(hue, saturation, lightness)

    def to_rgb(self) -> RGBColor:
        red, green, blue = colorsys.hls_to_rgb(
            self.hue, self.lightness, self.saturation
        )
        return RGBColor(red, green, blue)

    def to_ints(self) -> tuple[int, int, int]:
        return (
            int(self.hue * 360),
            int(self.saturation * 100.0),
            int(self.lightness * 100.0),
        )

    @classmethod
    def from_ints(cls, *args: int):
        hue = args[0] / 360.0
        saturation = args[1] / 100.0
        lightness = args[2] / 100.0
        return cls(hue, saturation, lightness)
