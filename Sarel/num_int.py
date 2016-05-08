from EW_lines import oiii_num
import csv
from os import listdir
import numpy as np
import pickle
import time

start = time.time()

# make a list of the file names and delete the first file (hidden)
fnames = listdir('./new_fits/boss400/after division')
del fnames[0]


# make a function that gives a list of EW of a file
def ewlist(fname):
    data = pickle.load(open('./new_fits/boss400/after division/%s' % fname, 'rb'))
    ew_exp = [0] * len(data)
    for i in range(len(data)):
        ew_exp[i] = oiii_num(data[i][0], data[i][1])
    ew_exp.insert(0, fname)
    return ew_exp


# def SNlist(fname):
#     data = pickle.load(open('./new_fits/after division/%s' % fname, 'rb'))
#     sn_exp = [0] * len(data)
#     for i in range(len(data)):
#         sn_exp[i] = SN(data[i][0], data[i][1], 3737)
#     sn_exp.insert(0, fname)
#     sn_avg = np.average(sn_exp[1:len(sn_exp)])
#     return sn_exp, sn_avg


# write the labels in the csv files
fl = open('./new_fits/boss400/oiii_num.csv', 'w')
writer = csv.writer(fl)
writer.writerow(['File Name', 'Exp 1', 'Exp 2', 'Exp 3', 'Exp 4',
                 'Exp 5', 'Exp 6', 'Exp 7', 'Exp 8', 'Exp 9', 'Exp 10',
                 'Exp 11', 'Exp12'])

fl2 = open('./new_fits/boss400/oiii_num problems.csv', 'w')
writer2 = csv.writer(fl2)
writer2.writerow(['problematic files'])

# loop through the files and insert into the csv
for i in range(len(fnames)):
    try:
        list1 = ewlist(fnames[i])
        writer.writerow(list1)
    # std_list = []
    # for j in range(1, len(list1)):
    #     std_list.append(list1[j])
    # std = np.std(std_list)
    # average = np.average(std_list)

    except Exception:
        writer2.writerow([fnames[i]])
    '''print('Problem with %s' % fnames[i])'''

fl.close()
fl2.close()

print('It took', time.time() - start, 'seconds')
