from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import erf


def create_absorption_line(bin_size, max_line_width, line_offset, area):
    """

    :param bin_size: bin size in wavelength units
    :param max_line_width: extents of the grid in wavelength units (on each side)
    :param line_offset: amount in wavelength units to shift the peak from 0
    :param area: profile area in wavelength units (* dimensionless flux)
    :return:
    """
    #

    # create an array large enough to reach at least max_line_width on both sides.
    ar_erf_wavelength = np.arange(0, 2 * max_line_width + 2 * bin_size, bin_size)
    # choose limits such that after numeric differentiation they are centered on 0.
    ar_erf_wavelength = ar_erf_wavelength - ar_erf_wavelength[ar_erf_wavelength.size // 2 - 1] - bin_size / 2
    # compute the error function
    ar_erf = erf(ar_erf_wavelength / area - line_offset) * area
    # differentiate the error function to get an area preserving gaussian.
    # after differentiation the wavelength values are shifted.
    ar_diff_wavelength = ar_erf_wavelength[:-1] + bin_size / 2
    ar_gaussian_profile = np.diff(ar_erf) / 2 / bin_size
    return ar_diff_wavelength, ar_gaussian_profile


test_bin_size = 0.64
# max_line_width should be far enough so that the area of the gaussian outside the boundary is 0.
# note that line_offset should probably be 0 for our use.

ar_wavelength, ar_profile = create_absorption_line(
    bin_size=test_bin_size, max_line_width=10, line_offset=5.0, area=0.0654)
# verify that the area under the gaussian is correct
print("area:", ar_profile.sum() * test_bin_size)
plt.plot(ar_wavelength, 1 - ar_profile)
plt.show()
