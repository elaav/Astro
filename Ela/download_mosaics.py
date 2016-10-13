# -*- coding: utf-8 -*-
"""
Created on Wed Mar 09 18:06:26 2016

@author: goddess
"""

import urllib2
import json
import os
import traceback, functools
import logging
import sys
import tarfile

root = logging.getLogger()
if not getattr(root, 'handler_set', None):
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    root.handler_set = True

# import argparse
#
# def parse_args():
#     parser = argparse.ArgumentParser(description='Downloading mosaics through SDSS web interface.')
#     parser.add_argument('-o', '--output', help='The output path', required=True)
#     parser.add_argument('-r', '--ra', help='The galaxy RA', required=True)
#     parser.add_argument('-d', '--dec', help='The galaxy dec', required=True)
#     parser.add_argument('-f', '--filters',help='The images filters (\'ugriz\')', default='ugriz')
#     parser.add_argument('-s', '--size',help='The image size', default=0.005)
#     return parser.parse_args()

def trace_unhandled_exceptions(func):
    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            print 'Exception in '+func.__name__
            traceback.print_exc()
    return wrapped_func


# parsing the json file from the SDSS sql interface
def parse_input(file_path):
    with open(file_path) as data_file:
        return json.load(data_file)[0][u'Rows']

# concating the url request
def create_request(ra, dec, filters, size):
    request_url='http://mirror.sdss3.org/mosaic-server/mosaic?onlyprimary=True&pixelscale=0.396'
    request_url = '&'.join([request_url,'ra='+str(ra),'dec='+str(dec),'filters='+filters,'size='+str(size)])
    return request_url

# gets galaxy object and downloading the mosaic to the given output path.
@trace_unhandled_exceptions
def get_mosaic(galaxy, output_path):
    objid = galaxy[u'objid']
    ra = galaxy[u'ra']
    dec = galaxy[u'dec']
    size=galaxy[u'petroRad_g']/3660  #TODO make sure it is the right conversion
    url = create_request(ra, dec, 'g', size)
    tmp_dir = 'tmp'
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    tmp_path = os.path.join(tmp_dir, str(objid) + '.tar')
    download_tar(url, tmp_path)
    extract_fit(tmp_path, output_path)


# downloading the zip file from the mosaics interface
def download_tar(request_url, output_path):
    logging.debug("Fetching the tar file from SDSS")
    req = urllib2.Request(request_url)
    req.add_header('Referer', 'http://data.sdss3.org/mosaics/check')
    resp = urllib2.urlopen(req)

    # saving tar
    file_name = output_path #OUTPUT_DIR+r'\new_test.tar'
    f = open(file_name, 'wb')
    meta = resp.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    #print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = resp.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        #status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        #status = status + chr(8)*(len(status)+1)
        #print status,

    f.close()

# extracting the fit out of the tar file
def extract_fit(tar_path, output_path):
    tar = tarfile.open(tar_path)
    member = tar.getmember(tar.getmembers()[0].name)
    member.name = os.path.basename(member.name)
    logging.debug("Extracting object id: %s" % member.name)
    tar.extractall(os.path.dirname(output_path))
    tar.close()
    os.remove(tar_path)

# prepering the request
# ra='171.44091'
# dec='4.82184'
# filters='g'
# size='0.005'

# def main():
#     args = parse_args()
#     ra = args.ra
#     dec = args.dec
#     size = args.size
#     filters = args.filters
#     path = args.output
#     request_url = create_request(ra, dec, filters, size)
#     download_tar(request_url, path)
#
# if __name__ == "__main__":
#     main()

#TODO download all galaxies, changing the size by radi field (arcsec to deg 3600)
#TODO open tar and save the fit with understandable name
#TODO create sql request to fetch data
#TODO stack images

"""
1) galaxies with spectroscopy (so we have the precise redshift)
2) pick a subset with similar size, profile, redshift, and orientation, so that we need to do almost nothing to stack them.
3) stack them.
"""





