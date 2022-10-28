import pytest

from color.cie.lab import CIELABColor
from color.cie.xyz import CIEXYZColor


def test_cielab_create():
    lab = CIELABColor()
    assert lab.L == 0.0
    assert lab.a == 0.0
    assert lab.b == 0.0


def test_cielab_to_xyz():
    lab = CIELABColor(46.140, -9.413, 8.219)

    xyz = lab.to_xyz()
    assert xyz.X == pytest.approx(0.13123, abs=0.0001)
    assert xyz.Y == pytest.approx(0.15372, abs=0.0001)
    assert xyz.Z == pytest.approx(0.13174, abs=0.0001)


def test_xyz_to_cielab():
    xyz = CIEXYZColor(0.13123, 0.15372, 0.13174)

    lab = CIELABColor.from_xyz(xyz)
    assert lab.L == pytest.approx(46.140, abs=0.001)
    assert lab.a == pytest.approx(-9.413, abs=0.001)
    assert lab.b == pytest.approx(8.219, abs=0.001)
