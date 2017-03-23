def full(b_num, r_num, filename):
    import pyfits as pf
    from scipy.signal import savgol_filter, medfilt
    import numpy
    import scipy.interpolate as inter
    from math import ceil

    # create the path of the fits file.
    path_fits = '%s' % filename

    # input all the data into different variables for ease of use.
    # for now, two vars, one for the blue and one for the red.
    b_data = pf.getdata(path_fits, b_num)
    r_data = pf.getdata(path_fits, r_num)
    b_flux = b_data['flux']
    b_wl = 10 ** b_data['loglam']
    r_flux = r_data['flux']
    r_wl = 10 ** r_data['loglam']

    # now take the mask for the pixels in the spectra for each part and filter out the bad pixels
    b_mask = b_data['mask']
    r_mask = r_data['mask']
    # b_where1 = numpy.where(b_mask == 0)
    # b_where2 = numpy.where(b_mask == 16)
    # b_mask = numpy.union1d(b_where1[0], b_where2[0])
    # r_where1 = numpy.where(r_mask == 0)
    # r_where2 = numpy.where(r_mask == 16)
    # r_mask = numpy.union1d(r_where1[0], r_where2[0])

    for i in range(len(b_flux)):
        if b_mask[i] != 0 and b_mask[i] != 16:
            b_flux[i] = None

    for i in range(len(r_flux)):
        if r_mask[i] != 0 and r_mask[i] != 16:
            r_flux[i] = None

    # b_flux = b_flux[b_mask]
    # b_wl = b_wl[b_mask]
    # r_flux = r_flux[r_mask]
    # r_wl = r_wl[r_mask]

    # we need to reverse the arrays if needed
    if b_wl[0] > b_wl[1]:
        b_flux = b_flux[::-1]
        b_wl = b_wl[::-1]

    if r_wl[0] > r_wl[1]:
        r_flux = r_flux[::-1]
        r_wl = r_wl[::-1]

    # we interpolate the blue and red parts so we can create one single continuum
    b_f = inter.interp1d(b_wl, b_flux)
    r_f = inter.interp1d(r_wl, r_flux)

    # now we can create new x and y vectors for both parts, using the interpolation.
    # this way we can make sure everything is consistent
    b_wl = numpy.arange(ceil(b_wl[0]), b_wl[len(b_wl) - 1], 0.5)
    r_wl = numpy.arange(ceil(r_wl[0]), r_wl[len(r_wl) - 1], 0.5)
    b_flux = b_f(b_wl)
    r_flux = r_f(r_wl)

    # find out what value is the first one in the red x vector (wavelength)
    # and what value is the last one of the blue x vector
    # these are the limits of the overlap
    first_r = r_wl[0]
    last_b = b_wl[len(b_wl)-1]

    # get what the limits are in terms of both parts' indices
    for i in range(len(b_wl) - 1):
        if b_wl[i] == first_r:
            first_b_i = i
            break

    for i in range(len(r_wl) - 1):
        if r_wl[i] == last_b:
            last_r_i = i
            break

    # create the unified overlap part
    y_over = numpy.zeros(last_r_i + 1)
    for i in range(last_r_i + 1):
        y_over[i] = numpy.median([b_flux[first_b_i + i], r_flux[i]])

    # create the unified vectors and apply filters
    x_con = numpy.arange(min(b_wl), max(r_wl) + 0.5, 0.5)
    y_con = numpy.hstack((b_flux[:first_b_i], y_over))
    y_con = numpy.hstack((y_con, r_flux[last_r_i + 1:]))

    # this is the smoothing
    '''
    y_con_filt = medfilt(y_con, 11)
    y_con = savgol_filter(y_con, 49, 11)
    '''

    # maybe for future use
    '''
    # now that we have the unified vectors we can interpolate and replace
    # the x vector with our single x vector we will use for every spectrum
    # inter_flux = inter.interp1d(x_con, y_con)
    # x_wl = numpy.arange(3200, 10000, 0.5)
    # y_flux = inter_flux(x_wl)
    '''

    return x_con, y_con
