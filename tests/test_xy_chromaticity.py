import pytest

from color.cie import UVChromaticity, XYChromaticity


def test_xy_chromaticity_z():
    xyc = XYChromaticity(0.25, 0.25)

    assert xyc.z == 0.5


def test_xy_chromaticity_from_uv():
    uvc = UVChromaticity(0.25, 0.25)

    xyc = XYChromaticity.from_uv(uvc)

    assert xyc.x == pytest.approx(0.236842105)
    assert xyc.y == pytest.approx(0.105263158)
    assert xyc.z == pytest.approx(0.657894737)
