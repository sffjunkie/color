import pytest

from color.hsv import HSVColor
from color.rgb import RGBColor


def test_hsv_from_ints():
    hsv = HSVColor.from_ints(120, 50, 30)
    assert hsv.hue == pytest.approx(1 / 3)
    assert hsv.saturation == 0.5
    assert hsv.value == 0.3


def test_hsv_to_ints():
    hsv = HSVColor.from_ints(120, 50, 30)
    data = hsv.to_ints()
    assert data[0] == 120
    assert data[1] == 50
    assert data[2] == 30


def test_hsv_to_rgb():
    hsv = HSVColor(120.0 / 360.0, 66.6666 / 100.0, 45.0 / 100.0)
    rgb = hsv.to_rgb()
    assert rgb.red == pytest.approx(0.15, abs=0.0001)
    assert rgb.green == pytest.approx(0.45, abs=0.0001)
    assert rgb.blue == pytest.approx(0.15, abs=0.0001)


def test_hsv_from_rgb():
    rgb = RGBColor(0.15, 0.45, 0.15)
    hsv = HSVColor.from_rgb(rgb)
    assert hsv.hue == pytest.approx(1 / 3)
    assert hsv.saturation == pytest.approx(2 / 3)
    assert hsv.value == pytest.approx(0.45)
