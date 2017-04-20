import pickle
from zipfile import ZipFile
import sys
import os
from glob import glob
import multiprocessing
from joblib import Parallel, delayed


dir = sys.argv[1]
dic = pickle.load(open("affirm_reverse.pkl", 'rb'))

os.chdir(dir)

zipfiles = glob('*zip')

count = 0
total = 0


def file_count(zfname):
    global count, total
    year = zfname[:-4]
    if int(year) < 1975:
        return

    zfile = ZipFile(zfname)
    members = zfile.namelist()

    for fname in members:

        if not fname.endswith('-maj.txt'):
            continue

        total += 1
        caseid = fname.split('/')[-1][:-8]

        case = dic.loc[dic['caseid'] == caseid]

        if case.empty:
            print("%s/%s" % (year + "_complete", caseid))
            continue

        count += 1
    print(count, total)


if __name__ == '__main__':
    num_cores = multiprocessing.cpu_count()
    Parallel(n_jobs=num_cores)(delayed(file_count)(f) for f in zipfiles)
