import string
import pickle
import os
import glob

from shutil import copyfile

df = pickle.load(open("district_affirm_reverse.pkl", "rb"))

print(df.shape)

duplicates = dict()
count = 0

for index, row in df.iterrows():

    docid = row["caseid"]
    folder = row["folder"]
    fname = "%s/%s" % (docid, folder)
    # fname += ".txt"

    if fname in duplicates.keys():
        print(fname)
        files = glob.glob("Pickles/*.pkl")

        for file in files:

            with open(file, "rb") as f:

                dic = pickle.load(f)

                for circ_id in dic.keys():

                    if fname in dic[circ_id]:

                        print(circ_id, f)

        count += 1
    else:
        duplicates[fname] = 1

    if count > 10:
        break
