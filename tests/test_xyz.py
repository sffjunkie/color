from color.cie.xyz import xyz_normalized_primary_matrices


def test_srgb_conversion():
    to_xyz, to_rgb = xyz_normalized_primary_matrices("sRGB")
