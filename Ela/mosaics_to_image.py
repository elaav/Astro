"""
Created on Wed Mar 09 16:38:43 2016

@author: goddess
"""

import pyfits
import matplotlib.pyplot as plt
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(description='Converting mosaics to images.')
    parser.add_argument('-o', '--output', help='The output file/dir path', required=True)
    parser.add_argument('-i', '--input', help='The input dir path', required=True)
    return parser.parse_args()

# Parsing the fits file and saves it to output_dir
def parse_fits_file(fits_file, output_dir):
    j_img = pyfits.getdata(fits_file)
    plt.imshow(j_img, aspect='equal')
    plt.title('image')
    #plt.show()
    image_path = os.path.join(output_dir, os.path.splitext(os.path.basename(fits_file))[0] + '.png')
    plt.savefig(image_path)


def main():
    args = parse_args()
    input = args.input
    output = args.output
    if os.path.isdir(input):
        mosaics = [os.path.join(input, p) for p in os.listdir(input)]
    else:
        mosaics = [input]
    for m in mosaics:
        parse_fits_file(m, output)


if __name__ == "__main__":
    main()

