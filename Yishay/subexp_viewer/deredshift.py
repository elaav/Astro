def deredshift(path, xaxis):
    import pyfits as pf

    # open the file to get the z value
    z = pf.getdata(path, 2)['z']
    for i in range(len(xaxis)):
        xaxis[i] = xaxis[i]/(z + 1)

    # return the new x-axis
    return xaxis