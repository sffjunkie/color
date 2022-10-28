import pytest

from color.hsl import HSLColor
from color.rgb import RGBColor


def test_hsl_from_ints():
    hsl = HSLColor.from_ints(120, 50, 30)
    assert hsl.hue == pytest.approx(1 / 3)
    assert hsl.saturation == 0.5
    assert hsl.lightness == 0.3


def test_hsl_to_ints():
    hsl = HSLColor.from_ints(120, 50, 30)
    data = hsl.to_ints()
    assert data[0] == 120
    assert data[1] == 50
    assert data[2] == 30


def test_hsl_to_rgb():
    hsl = HSLColor(120.0 / 360.0, 50.0 / 100.0, 30.0 / 100.0)
    rgb = hsl.to_rgb()
    assert rgb.red == pytest.approx(0.15)
    assert rgb.green == pytest.approx(0.45)
    assert rgb.blue == pytest.approx(0.15)


def test_hsl_from_rgb():
    rgb = RGBColor(0.15, 0.45, 0.15)
    hsl = HSLColor.from_rgb(rgb)
    assert hsl.hue == pytest.approx(1 / 3)
    assert hsl.saturation == pytest.approx(0.5)
    assert hsl.lightness == pytest.approx(0.3)
