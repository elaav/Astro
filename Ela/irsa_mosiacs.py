# -*- coding: utf-8 -*-
"""
Created on Wed Mar 09 18:06:26 2016

@author: goddess
"""

import time
import urllib
import argparse
from xml.dom import minidom

URL_IRSA='http://irsa.ipac.caltech.edu/cgi-bin/FinderChart/nph-finder'

def parse_args():
    parser = argparse.ArgumentParser(description='Downloading mosaics throgh IRSA web interface.')
    parser.add_argument('-o', '--output', help='The output path', required=True)
    parser.add_argument('-r', '--ra', help='The galaxy RA', required=True)
    parser.add_argument('-d', '--dec', help='The galaxy dec', required=True)
    parser.add_argument('-s', '--size',help='The image size (in range [1,6])', required=True)
    return parser.parse_args()


def download_mosaic_irsa(filename, ra, dec, size):
  """
  Downloading mosaics from SDSS by IRSA web interface.
  size is in range [1,6]!
  """
  coord = ra + " " + dec
  parameters={"mode": "prog", "locstr": coord, "subsetsize": size, \
  "survey": "SDSS", "orientation": "left", "reproject": "false", "grid_orig": "false", \
  "grid_shrunk": "false", "markervis_orig": "true", "markervis_shrunk": "true"}
  # connection to IRSA
  print "# Retrieving image information from IRSA"
  t1 = time.time()
  url_data = urllib.urlencode(parameters)
  res = urllib.urlopen(URL_IRSA, url_data)
  t2 = time.time()
  print "... %f seconds" % (t2 - t1)
  # extraction of XML data
  use_dom = minidom.parse(res)
  temp = use_dom.getElementsByTagName('finderchart')
  temp = temp[0]
  status_value = temp.attributes["status"].value
  if status_value != "ok":
    print "... failed with finderchart status=",status_value
    return 1
  temp = use_dom.getElementsByTagName('totalimages')
  temp = temp[0]
  number_of_images = int(temp.firstChild.data)
  print "# the number of images = %d " % (number_of_images)
  i = 1
  for image_node in use_dom.getElementsByTagName('image'):
    str_ind = "%02d" % (i)
    survey = image_node.getElementsByTagName('surveyname')
    survey = survey[0].firstChild.data
    survey = survey.strip()
    band = image_node.getElementsByTagName('band')
    band = band[0].firstChild.data
    band = band.strip()
    # FITS files
    fits_url = image_node.getElementsByTagName('fitsurl')
    fits_url = fits_url[0].firstChild.data
    fits_url = fits_url.strip()
    out_fn_fits = filename+"_"+str_ind+"_"+survey+"_"+band+".fits"
    print "..."+out_fn_fits
    urllib.urlcleanup()
    t1 = time.time()
    urllib.urlretrieve(fits_url, out_fn_fits)
    t2 = time.time()
    i = i + 1


if __name__=="__main__":
    args = parse_args()
    ra = args.ra
    dec = args.dec
    size = args.size
    path = args.output
    download_mosaic_irsa(path, ra, dec, size)




