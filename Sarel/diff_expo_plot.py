def draw(*args):
    from full_func import full
    from deredshift import deredshift
    from time_steps import time_steps
    import matplotlib.pyplot as plt
    import matplotlib.cm as cmap
    import pyfits as pf

    # get the path of the fits file
    if type(args[0]) != str:
        plate = str(args[0]).zfill(4)
        mjd = args[1]
        fiber = str(args[2]).zfill(4)
        path_fits = '/Users/sarelg/gastro/sdss/files/spec-%s-%d-%s.fits' % (plate, mjd, fiber)
    else:
        path_fits = '/Users/sarelg/gastro/sdss/files/%s' % args[0]

    # get the number of exposures
    num_exp = int((pf.getheader(path_fits, 0)['nexp'])/2)

    # create the data, a list of all the sub-exposures
    data = [0]*num_exp
    for i in range(num_exp):
        x, y = full(i + 4, i + 4 + num_exp, path_fits)
        x = deredshift(path_fits, x)
        tup = x, y
        data[i] = tup

    # plot all of the exposures using a different color for each one
    colorm = cmap.get_cmap('autumn')
    cm_num = int(256/num_exp)
    label = time_steps(path_fits, num_exp)
    for i in range(len(data)):
        plt.plot(data[i][0], data[i][1], color=colorm(i*cm_num),
                 label=label[i], linewidth=0.5)
        plt.legend(prop={'size': 11})

    # plt.show()


def cor_exp(*args):
    from full_func import full
    from deredshift import deredshift
    import pyfits as pf

    # get the path of the fits file
    if type(args[0]) != str:
        plate = str(args[0]).zfill(4)
        mjd = args[1]
        fiber = str(args[2]).zfill(4)
        path_fits = './new_fits/boss400/files/spec-%s-%d-%s.fits' % (plate, mjd, fiber)
    else:
        path_fits = './new_fits/boss400/files/%s' % args[0]

    # get the number of exposures
    num_exp = int((pf.getheader(path_fits, 0)['nexp'])/2)

    # create the data, a list of all the sub-exposures
    data = [0]*num_exp
    for i in range(num_exp):
        x, y = full(i + 4, i + 4 + num_exp, path_fits)
        x = deredshift(path_fits, x)
        tup = [x, y]
        data[i] = tup

    return data


def outline(fits_file):
    from EW_lines import oii
    import numpy as np

    data = cor_exp(fits_file)

    ew = [0]*len(data)

    for i in range(len(data)):
        ew[i] = oii(data[i][0], data[i][1])[0]

    ew_std = np.std(ew)
    ew_avg = np.mean(ew)

    out = 0
    for i in range(len(ew)):
        if abs(ew[i] - ew_avg) > 3*ew_std:
            print(ew[i], 'in', fits_file)
            out += 1

    if out == 0:
        print('No outliers in', fits_file)
