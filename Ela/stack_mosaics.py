"""
* to make the scale more flexsible to move by less than pixel interpolation (in principle they only need to be aligned,
probably better if interpolated to a denser grid in the process)
    # http://docs.scipy.org/doc/scipy/reference/tutorial/interpolate.html
* make the query to sloan for 1000 objects
* we can verify by testing that the noise does behave like sqrt(N)

* make post download validation
* create synthetic data to make sure our similar validation is good: take one galaxy and add noise  to it
"""

import numpy as np
import scipy.ndimage
import pyfits


def interpolate_fits(fits_file):
    origin_fits = pyfits.getdata(fits_file)
    zoomed_fits = scipy.ndimage.zoom(origin_fits, 4)
    #new_j = interp.shift(old_j, [shiftY, shiftX])
    import matplotlib.pyplot as plt

    plt.imshow(zoomed_fits, aspect='equal')
    plt.title('image')
    plt.show()





if __name__ == '__main__':
    interpolate_fits('fits/J120412.00+343604.0-g.fits')