import csv
import wget

# open the csv file and skip the first row (the names of the columns)
with open('./BOSS400.csv') as f:
    reader = csv.reader(f)
    reader.__next__()

    # put all of the necessary data into variables
    for row in reader:
        instrument = row[5].lower()
        plate4 = str(row[0])
        plate4 = plate4.zfill(4)
        mjd = row[1]
        fiberid4 = str(row[2])
        fiberid4 = fiberid4.zfill(4)

        if instrument == 'sdss':

            if int(plate4) >= 3000:
                run2d = '104'

            elif int(plate4) <= 2974:
                run2d = '26'

        elif instrument == 'boss':
            run2d = 'v5_7_0'

        # get the data files
        try:
            url = 'http://data.sdss3.org/sas/dr12/%s/spectro/redux/%s/spectra/%s/spec-%s-%s-%s.fits' \
                  % (instrument, run2d, plate4, plate4, mjd, fiberid4)
            file_name = wget.download(url, './new_fits/boss400/files')

        except Exception:
            print('spec-%s-%s-%s.fits not found' % (plate4, mjd, fiberid4))