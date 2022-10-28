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

    def to_ints(self) -> tuple[int, int, int]:
        return (
            int(self.hue * 360),
            int(self.saturation * 100.0),
            int(self.value * 100.0),
        )

    @classmethod
    def from_ints(cls, *args: int):
        hue = args[0] / 360.0
        saturation = args[1] / 100.0
        value = args[2] / 100.0
        return cls(hue, saturation, value)
