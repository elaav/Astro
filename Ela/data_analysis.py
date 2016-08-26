import matplotlib.pyplot as plt
import os
import pyfits
import math


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
        fig = plt.figure(i)
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
            p += 1

        fig.subplots_adjust(wspace=0.01, hspace=0.01)
        #plt.show()'
        plt.savefig(os.path.join(output_dir, str(key) + '.png'))
        i += 1