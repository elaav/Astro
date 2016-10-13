from PyAstronomy import pyasl

def dec_decimal_to_sexagesimal(dec):
    h = int(dec)
    ms = (dec - h) * 60
    m = int(ms)
    s = (ms - m) * 60
    return h, m, s

def dec_sexagesimal_to_decimal(hour, minute, second):
    ms = (second / 60) + minute
    return (ms / 60) + hour

def ra_decimal_to_sexagesimal(dec):
    h = int(dec)
    ms = (dec - h) * 60
    m = int(ms)
    s = (ms - m) * 60
    return h, m, s

def coordsSexaToDeg(ra_dec):
    try:
        return pyasl.coordsSexaToDeg(ra_dec)
    except:
        ra, dec = ra_dec.split('+')
        ra = pad_with_spaces(ra)
        dec = pad_with_spaces(dec)
        ra_dec = ra + ' +' + dec
        return pyasl.coordsSexaToDeg(ra_dec)

def pad_with_spaces(s):
    # padding string in sexagesimal with spaces
    ind = s.find('.')
    return s[:ind - 4] + ' ' + s[ind - 4:ind - 2] + ' ' + s[ind - 2:]

def raw_to_skycoor(ra_dec):
    spliter = None
    if '-' in ra_dec:
        spliter = '-'
    elif '+' in ra_dec:
        spliter = '+'
    if spliter:
        ra, dec = ra_dec.split(spliter)
        ind = ra.find('.')
        ra = ra[:ind - 4] + 'h' + ra[ind - 4:ind - 2] + 'm' + ra[ind - 2:] + 's'
        ind = dec.find('.')
        dec = dec[:ind - 4] + 'd' + dec[ind - 4:ind - 2] + 'm' + dec[ind - 2:] + 's'
        return ra + spliter + dec
    return ra_dec