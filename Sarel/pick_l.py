from diff_expo_plot import cor_exp
import pickle
from os import listdir
from EW_lines import continuum
import numpy as np

# list all the files in the folder
fnames = listdir('./new_fits/boss400/files')
del fnames[0]

# pickle to three different folders the continuum fits, divided spectra and raw fits
for i in range(len(fnames)):
    try:
        cor = cor_exp(fnames[i])
        sub_con = np.copy(cor)
        sub_fit = np.copy(cor)
        pickle.dump(cor, open('./new_fits/boss400/sub exposures/%s.p' % fnames[i], 'wb'))
        for j in range(len(sub_con)):
            sub_con[j][1], sub_fit[j][1] = continuum(cor[j][0], cor[j][1], is_new=True)
        pickle.dump(sub_con, open('./new_fits/boss400/after division/%s.p' % fnames[i], 'wb'))
        pickle.dump(sub_fit, open('./new_fits/boss400/just cont/%s.p' % fnames[i], 'wb'))
    except Exception:
        print('Problem with %s' % fnames[i])