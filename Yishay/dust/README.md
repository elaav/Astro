## sfd_lookup.py

### SFDLookup:
This class retrieves the extinction values for given sky locations from the SFD maps.

#### Requirements:
Two `.fits` files from the Schlegel-Finkbeiner-Davis data.  
At the time of writing they are available from:  
http://nebel.rc.fas.harvard.edu/mjuric/lsd-data/sfd-dust-maps/

The full resolution files are:
```
SFD_dust_4096_ngp.fits
SFD_dust_4096_sgp.fits
```
(NGP and SGP stand for North and South Galactic Pole)

#### How to use:
- The class initializer takes 2 arguments for the NGP and SGP files.
- The `lookup_*()` methods accept 2 1D numpy arrays of galactic *l* and *b* parameters.
- The returned array contains the extinction levels.
- `lookup_linear` closely matches the SDSS extinction values in CasJobs (up to a factor).

#### Example:
Assume we have `ra` and `dec` arrays, and that the filename variables have been set correctly.  
Typical usage would be something like:

```python
from sfd_lookup import SFDLookUp
from astropy.coordinates import SkyCoord

sfd = SFDLookUp(ngp_filename, sgp_filename)

coordinates_icrs = SkyCoord(ra=ra, dec=dec)
coordinates_galactic = coordinates_icrs.galactic
extinction_values = sfd.lookup_linear(coordinates_galactic.l.to(u.rad).value,
                                      coordinates_galactic.b.to(u.rad).value)
```
