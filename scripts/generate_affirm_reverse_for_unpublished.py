import pickle
from zipfile import ZipFile
import sys
import os
from glob import glob
import re
import multiprocessing
from joblib import Parallel, delayed


dir = sys.argv[1]
dic = pickle.load(open("affirm_reverse.pkl", 'rb'))

file_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(file_path, os.pardir)
os.chdir(dir)

zipfiles = glob('*zip')
zipfiles = sorted(zipfiles)

count = 0
total = 0

affirm_reverse_dict = {}
affirm_list = ["affirmed", "affirm", "affirming", "affirms", "dismissed"]
reverse_list = ["reversed", "reverse", "reversing", "reverses", "reversal"]


def set_affirm_reverse(zfname):
    global count, total
    year = zfname[:-4]
    if int(year) < 1924:
        return
    print(year)

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
        status = ""
        if case.empty and caseid in match_dic:
            data = zfile.read(fname).decode()
            data = re.sub(r'![\W\s_]+', "", data)
            data = data.lower().split(" ")
            for i in affirm_list:
                if i in data:
                    status = "Affirmed"
                    break

            for i in reverse_list:
                if i in data:
                    if status == "Affirmed":
                        status = ""
                    else:
                        status = "Reversed"
                    break

            if len(status) == 0:
                continue
            else:
                print(caseid, status)
                affirm_reverse_dict[caseid] = status

    pickle.dump(affirm_reverse_dict, open("unpublished_affirm_reverse.pkl", "wb"))


if __name__ == '__main__':
    num_cores = multiprocessing.cpu_count()
    Parallel(n_jobs=num_cores)(delayed(set_affirm_reverse)(f) for f in zipfiles)
