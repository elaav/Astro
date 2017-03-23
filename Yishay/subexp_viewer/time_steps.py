def time_steps(path, num_exp):
    import pyfits as pf

    label = [0]*num_exp
    label[0] = '0 minutes'
    for i in range(num_exp - 1):
        label[i + 1] = str(round((pf.getheader(path, 4 + i + 1)['tai-beg'] -
                                  pf.getheader(path, 4)['tai-beg'])/60)) + ' minutes'
    return label
