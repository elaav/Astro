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
import argparse

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

def parse_args():
    parser = argparse.ArgumentParser(description='Downloading mosaics from SDSS in parallel')
    parser.add_argument('-j', '--jfile', help='JSON file with objid, ra, dec, petroRad_g', required=True)
    return parser.parse_args()

def load_objs(jfile):
    with open(jfile) as data_file:
        return json.load(data_file)[0][u'Rows']

if __name__ == '__main__':

    args = parse_args()
    jfile = args.jfile

    pool = Pool(processes=POOL_SIZE)              # start POOL_SIZE worker processes

    galaxies = load_objs(jfile)
    for galaxy in galaxies:
        logging.debug("Downloading object %s" % str(galaxy[u'objid']))
        output_path = os.path.join(FITS_DIR, str(galaxy[u'objid'])+time.strftime("_%Y%m%d-%H%M"))
        result = pool.apply_async(dm.get_mosaic, [galaxy,output_path])    # evaluate get_mosaic asynchronously

    pool.close()
    pool.join()

    logging.info("Downloading ended successfully")

    #fits = [os.path.join(FITS_DIR,f) for f in os.listdir(FITS_DIR)]
    # for fits_file in fits:
    #     parse_fits_file(fits_file, "")



