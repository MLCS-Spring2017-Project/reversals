import pickle
from zipfile import ZipFile
import sys
import os
from glob import glob
import multiprocessing
from joblib import Parallel, delayed


dir = sys.argv[1]
dic = pickle.load(open("affirm_reverse.pkl", 'rb'))

df = pickle.load(open("district_affirm_reverse.pkl", "rb"))

file_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(file_path, os.pardir)
os.chdir(dir)

zipfiles = glob('*zip')

count = 0
total = 0


def file_count(zfname):
    global count, total
    year = zfname[:-4]
    if int(year) < 1924:
        return

    zfile = ZipFile(zfname)
    members = zfile.namelist()
    pickle_file = "%s_95.pkl" % year
    pickle_file = os.path.join(file_path, "pickles", pickle_file)
    with open(pickle_file, "rb") as f:
        match_dic = pickle.load(f)
    for fname in members:

        if not fname.endswith('-maj.txt'):
            continue

        total += 1
        caseid = fname.split('/')[-1][:-8]

        case = dic.loc[dic['caseid'] == caseid]

        if case.empty and caseid in match_dic:
            print("%s/%s" % (year + "_complete", caseid), match_dic[caseid])
            count += 1
            continue

    print(count, total)


if __name__ == '__main__':
    num_cores = multiprocessing.cpu_count()
    Parallel(n_jobs=num_cores)(delayed(file_count)(f) for f in zipfiles)
