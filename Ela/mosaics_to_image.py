# -*- coding: utf-8 -*-
"""
Created on Wed Mar 09 16:38:43 2016

@author: goddess
"""

import pyfits
import matplotlib.pyplot as plt
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Downloading mosaics throgh IRSA web interface.')
    parser.add_argument('-o', '--output', help='The output path', required=True)
    parser.add_argument('-i', '--input', help='The input path', required=True)
    return parser.parse_args()

# Parsing the fits file
def parse_fits_file(fits_file, output_path):
    j_img = pyfits.getdata(fits_file)
    plt.imshow(j_img, aspect='equal')
    plt.title('image')
    plt.show()
    #py.savefig('my_rgb_image.png')


def main():
    args = parse_args()
    input = args.input
    output = args.output
    parse_fits_file(input, output)
    #TODO save to output path

if __name__ == "__main__":
    main()

