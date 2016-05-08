"""This function fits the contiuum of a spectrum and returns a y-vector
normalised by it"""


def continuum(x, y, is_new=False):
    import astropy.modeling as mod
    import numpy as np

    # xf1 = np.zeros(6300-5150)
    # yf1 = np.zeros(6300-5150)
    # xf2 = np.zeros(8000-7000)
    # yf2 = np.zeros(8000-7000)

    # find where the line-free area starts
    for i in range(len(x)):
        if x[i] >= 5150:
            x1_start_i = i
            break

    # where the line-free area stops
    for i in range(len(x)):
        if x[x1_start_i + i] >= 6300:
            x1_stop_i = x1_start_i + i
            break

    # create vectors and put the data inside
    xf1 = np.zeros(x1_stop_i - x1_start_i)
    yf1 = np.zeros(x1_stop_i - x1_start_i)

    for i in range(len(xf1)):
        xf1[i] = x[x1_start_i + i]
        yf1[i] = y[x1_start_i + i]

    # line-free area start
    for i in range(len(x)):
        if x[i] >= 7000:
            x2_start_i = i
            break

    # line-free area stops
    for i in range(len(x)):
        if x2_start_i + i == len(x) - 1 or x[x2_start_i + i] >= 8000:
            x2_stop_i = x2_start_i + i
            break

    # create vectors and insert data
    xf2 = np.zeros(x2_stop_i - x2_start_i)
    yf2 = np.zeros(x2_stop_i - x2_start_i)

    for i in range(len(xf2)):
        xf2[i] = x[x2_start_i + i]
        yf2[i] = y[x2_start_i + i]

    # make a single vector out of the line-free areas
    xf = np.hstack((xf1, xf2))
    yf = np.hstack((yf1, yf2))

    # fit a power law
    g_init = mod.models.PowerLaw1D(20, 5150, 0.5)
    fit_g = mod.fitting.LevMarLSQFitter()
    g = fit_g(g_init, xf, yf)

    # subtract the continuum
    y_con = np.zeros(len(x))
    for i in range(len(x)):
        y_con[i] = g(x[i])
        y[i] = y[i] / y_con[i]
    if not is_new:
        return y
    # if there is a need for the fit itself
    else:
        return y, y_con


"""this function calcualtes the equivalent width of the OII3272 line"""


def oii(x, y):
    import astropy.modeling as mod
    import numpy as np
    import scipy.integrate as int

    # subtract the contiuum
    y = continuum(x, y)

    # isolate the OII line
    for i in range(len(x)):
        if x[i] >= (3727 - 30):
            xfi = i
            break

    for i in range(len(x)):
        if x[i] >= (3727 + 30):
            xff = i
            break

    x1 = np.zeros(abs(xff - xfi))
    y1 = np.zeros(abs(xff - xfi))

    for i in range(len(x1)):
        x1[i] = x[xfi + i]
        y1[i] = y[xfi + i]

    # define the gaussian for the fit
    def cus_gauss(x, amplitude=1., mean=0., stddev=1.):
        return 1 + amplitude * np.exp(-((x - mean) ** 2) / (2 * (stddev ** 2)))

    cus_mod = mod.models.custom_model(cus_gauss)

    # perform the fit
    g_init = cus_mod(2, 3727, 1)
    fit_g = mod.fitting.LevMarLSQFitter()
    g = fit_g(g_init, x1, y1)

    # calcualte the equivalent width
    def integrand(x, amplitude, mean, stddev):
        return amplitude * np.exp(-((x - mean) ** 2) / (2 * (stddev ** 2)))

    xfit = np.arange(0., 10000., 1.)
    yfit = integrand(xfit, g.amplitude, g.mean, g.stddev)
    equwid = (int.simps(yfit))

    return equwid, g.amplitude / 1.0, g.mean / 1.0, g.stddev / 1.0


"""this function calcualtes the equivalent width of the SII6716, SII6731
 lines"""


def sii(x, y):
    import astropy.modeling as mod
    import numpy as np
    import scipy.integrate as int

    # subtract the contiuum
    y = continuum(x, y)

    # isolate the SII lines
    for i in range(len(x)):
        if x[i] >= (6716 - 30):
            xfi = i
            break

    for i in range(len(x)):
        if x[i] >= (6731 + 30):
            xff = i
            break

    x1 = np.zeros(abs(xff - xfi))
    y1 = np.zeros(abs(xff - xfi))

    for i in range(len(x1)):
        x1[i] = x[xfi + i]
        y1[i] = y[xfi + i]

    # define the gaussian for the fit
    def cus_gauss(x, amplitude=1., mean=0., stddev=1.):
        return 1 + amplitude * np.exp(-((x - mean) ** 2) / (2 * (stddev ** 2)))

    cus_mod = mod.models.custom_model(cus_gauss)

    # perform the fit
    g1 = cus_mod(1, 6716, 1)
    g2 = mod.models.Gaussian1D(1, 6731, 1)
    g_init = g1 + g2
    fit_g = mod.fitting.LevMarLSQFitter()
    g = fit_g(g_init, x1, y1)

    # calcualte the equivalent width
    def integrand(x, amplitude, mean, stddev):
        return amplitude * np.exp(-((x - mean) ** 2) / (2 * (stddev ** 2)))

    xfit = np.arange(0., 10000., 1.)
    yfit1 = integrand(xfit, g[0].amplitude, g[0].mean, g[0].stddev)
    yfit2 = integrand(xfit, g[1].amplitude, g[1].mean, g[1].stddev)
    equwid = [0] * 2
    equwid[0], equwid[1] = int.simps(yfit1), int.simps(yfit2)

    return equwid[0], equwid[1], g[0].amplitude / 1.0, g[1].amplitude / 1.0


"""this function calcualtes the equivalent width of the OIII5007 line"""


def oiii(x, y):
    import astropy.modeling as mod
    import numpy as np
    import scipy.integrate as int

    # subtract the contiuum
    y = continuum(x, y)

    # isolate the OIII line
    for i in range(len(x)):
        if x[i] >= (5007 - 30):
            xfi = i
            break

    for i in range(len(x)):
        if x[i] >= (5007 + 30):
            xff = i
            break

    x1 = np.zeros(abs(xff - xfi))
    y1 = np.zeros(abs(xff - xfi))

    for i in range(len(x1)):
        x1[i] = x[xfi + i]
        y1[i] = y[xfi + i]

    # define the gaussian for the fit
    def cus_gauss(x, amplitude=1., mean=0., stddev=1.):
        return 1 + amplitude * np.exp(-((x - mean) ** 2) / (2 * (stddev ** 2)))

    cus_mod = mod.models.custom_model(cus_gauss)

    # find out where the 5007 line is exactly and take the
    # amplitude for the initial guess
    for i in range(len(x)):
        if x[i] >= 5007:
            x_line = i
            break

    # perform the fit
    g_init = cus_mod(y[x_line], 5007, 1)
    fit_g = mod.fitting.LevMarLSQFitter()
    g_init.mean.fixed = True
    g_init.amplitude.bounds = [0, 1000]
    g = fit_g(g_init, x1, y1)

    # calcualte the equivalent width
    def integrand(x, amplitude, mean, stddev):
        return amplitude * np.exp(-((x - mean) ** 2) / (2 * (stddev ** 2)))

    xfit = np.arange(0., 10000., 1.)
    yfit = integrand(xfit, g.amplitude, g.mean, g.stddev)
    equwid = (int.simps(yfit))

    return equwid


"""This function calculates the S/N ratio for an exposure"""


def SN(x, y, line):
    import astropy.modeling as mod
    import numpy as np
    import matplotlib.pyplot as plt

    for i in range(len(x)):
        if x[i] >= (line + 10):
            xfi = i
            xff = i + 100
            break

    x1 = np.zeros(abs(xff - xfi))
    y1 = np.zeros(abs(xff - xfi))

    for i in range(abs(xff - xfi)):
        x1[i] = x[i + xfi]
        y1[i] = y[i + xfi]

    # fit a power law

    g_init = mod.models.PowerLaw1D(1, line + 10, 0.5)
    fit_g = mod.fitting.LevMarLSQFitter()
    g = fit_g(g_init, x1, y1)

    for i in range(len(x1)):
        y1[i] = y1[i] / g(x1[i])

    std = np.std(y1)

    S_N = 1 / std

    return S_N


'''This function calculates a numerical integral of a line'''


def oiii_num(x, y):
    import numpy as np

    # isolate the OIII line
    for i in range(len(x)):
        if x[i] >= (5007 - 30):
            xfi = i
            break

    for i in range(len(x)):
        if x[i] >= (5007 + 30):
            xff = i
            break

    x1 = np.zeros(abs(xff - xfi))
    y1 = np.zeros(abs(xff - xfi))

    for i in range(len(x1)):
        x1[i] = x[xfi + i]
        y1[i] = y[xfi + i]

    equwid = np.trapz(y1, x1)

    return equwid
