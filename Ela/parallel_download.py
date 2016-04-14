"""
Downloading mosaics from SDSS according to json file (output of SQL query)
"""

from multiprocessing import Pool
import download_mosaics as dm
import json
import time
import os
import logging
import sys
import pyfits
import matplotlib.pyplot as plt

root = logging.getLogger()
if not getattr(root, 'handler_set', None):
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    root.handler_set = True

POOL_SIZE = 4
TIMEOUT = 20
FITS_DIR = 'fits'

def load_objs(jfile):
    with open(jfile) as data_file:
        return json.load(data_file)[0][u'Rows']

# Parsing the fits file
def parse_fits_file(fits_file, output_path):
    j_img = pyfits.getdata(fits_file)
    plt.imshow(j_img, aspect='equal')
    plt.title('image')
    plt.show()
    #py.savefig('my_rgb_image.png')

if __name__ == '__main__':

    pool = Pool(processes=POOL_SIZE)              # start POOL_SIZE worker processes

    jfile = "data/galaxies.json"
    galaxies = load_objs(jfile)
    for galaxy in galaxies:
        logging.debug("Downloading object %s" % str(galaxy[u'objid']))
        output_path = os.path.join(FITS_DIR, str(galaxy[u'objid'])+time.strftime("_%Y%m%d-%H%M"))
        result = pool.apply_async(dm.get_mosaic, [galaxy,output_path])    # evaluate get_mosaic asynchronously

    pool.close()
    pool.join()

    fits = [os.path.join(FITS_DIR,f) for f in os.listdir(FITS_DIR)]
    # for fits_file in fits:
    #     parse_fits_file(fits_file, "")



