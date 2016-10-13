import matplotlib.pyplot as plt
import os
import pyfits
import math
from utils import coordsSexaToDeg, raw_to_skycoor
from astroquery.sdss import SDSS
from astropy import coordinates as coords
from astropy import units
import numbers

# Querying SDSS for object according to given coordinates (supporting 2 different coords formats)
def query_sdss(coor, radius=None):
    try:
        pos = coords.SkyCoord(coor, frame='icrs')
    except:
        pos = coords.SkyCoord(raw_to_skycoor(coor), frame='icrs')
    if not radius:
        radius = 20. * units.arcsec
    return SDSS.query_region(pos ,radius=radius, spectro=True)

# Converting SDSS mosaic name to decimal SkyCoord format
def file_name_to_skycoor(file_name):
    if file_name.count('-') == 1:
        return raw_to_skycoor(file_name[1:].split('-')[0])
    elif file_name.count('-') > 1:
        splitted = file_name[1:].split('-')
        return raw_to_skycoor(splitted[0] + '-' + splitted[1])

# Converting SDSS mosaic name to decimal coordinates
def file_name_to_decimal_coor(file_name):
    if file_name.count('-') == 1:
        return coordsSexaToDeg(file_name[1:].split('-')[0])
    elif file_name.count('-') > 1:
        splitted = file_name[1:].split('-')
        return coordsSexaToDeg(splitted[0] + '-' + splitted[1])

# Retrieving SDSS objid for given mosaic name
def file_name_to_objid(file_name):
    res = query_sdss(file_name_to_skycoor(file_name))
    if res:
        num = len(set(res.columns["objid"]))
        if num > 1:
            print "more than 1:", list(set(res.columns["objid"]))
        return res.columns["objid"][0], num
    print file_name, "was not found"
    return None, 0

def indexes_to_file_names(size, inds, fits_dir):
    fits = [os.path.join(fits_dir, p) for p in os.listdir(fits_dir) if p.endswith('.fits')]
    fits = [os.path.basename(fit) for fit in fits if pyfits.getdata(fit).size == size]
    names = {}
    for i in inds:
        names[i] = fits[i - 1]
    return names

def indexes_to_objids(size, inds_list, fits_path):
    objids = []
    file_names = indexes_to_file_names(size, inds_list, fits_path)
    for name in file_names.values():
        res = query_sdss(file_name_to_skycoor(name))
        if res:
            if len(set(res.columns["objid"])) > 1:
                print "more than 1:", list(set(res.columns["objid"]))
            objids.append(res.columns["objid"][0])
        else:
            print name, "was not found"
    return objids


def arrange_fits_by_size_with_name(fits_data):
    data_by_size = {}
    for f, name in fits_data:
        size = f.size
        if not data_by_size.has_key(size):
            data_by_size[size] = []
        data_by_size[size].append(f)

# Gets fits and returns dict of lists {size:[fits of size]}
def arrange_fits_by_size(fits_data):
    data_by_size = {}
    for f in fits_data:
        size = f.size
        if not data_by_size.has_key(size):
            data_by_size[size] = []
        data_by_size[size].append(f)

# gets the out of range properties according to the outliers.
# @param objects: list of dicts of regular objects (NO outliers)
# @param outliers: list of dicts of outliers objects
# @param limit: number of dots out of range
def get_different_properties(objects, outliers, limit):
    properties = objects[0].keys()
    keys = []
    for key in properties:
        good_vals = [obj.get(key) for obj in objects]
        bad_vals = [obj.get(key) for obj in outliers]
        if isinstance(good_vals[0], numbers.Number):
            gmax = max(good_vals)
            gmin = min(good_vals)
            cmin = 0
            cmax = 0
            for val in bad_vals:
                if val < gmin:
                    cmin += 1
                elif val > gmax:
                    cmax += 1
            if cmin == limit or cmax == limit:
                keys.append(key)
    return keys

# Plotting all fits together, separated by fits size
def plot_all_fits(fits_dir, output_dir):
    fits = [os.path.join(fits_dir, p) for p in os.listdir(fits_dir) if p.endswith('.fits')]
    fits_data = [pyfits.getdata(fit) for fit in fits]

    data_by_size = {}
    for f in fits_data:
        size = f.size
        if not data_by_size.has_key(size):
            data_by_size[size] = []
        data_by_size[size].append(f)

    i = 1
    for key, val in data_by_size.iteritems():
        print "At size:", key
        fig = plt.figure(i, (9, 9))
        plt.title('size = ' + str(key) + ' pixels')
        p = 1
        m = int(math.sqrt(len(val)))
        if math.sqrt(len(val)) != m:
            m += 1
        n = m
        for j_img in val:
            fig.add_subplot(m, n, p)
            plt.imshow(j_img)
            plt.axis('off')
            plt.annotate(str(p), xy=(1, 0), xycoords='axes fraction', fontsize=8,
                         xytext=(0, 0), textcoords='offset points',
                         ha='left', va='bottom')
            p += 1

        fig.subplots_adjust(wspace=1, hspace=0.01)
        pic_path = 'fits/' + str(key) + '.png'
        if os.path.isfile(pic_path):
            os.remove(pic_path)
        plt.savefig('fits/' + str(key) + '.png')
        i += 1