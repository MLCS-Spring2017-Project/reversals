import csv
import sys
import os
import pickle

from collections import Counter
from glob import glob
from zipfile import ZipFile

file = open(sys.argv[1], "rb")


entry = csv.reader(file)

i = 0
cases = {}
print(entry)

for row in entry:

    # parties = row[1].split("v.", 1)

    cases["name"] = row[1]
    # cases["Second_Person"] = parties[1]
    cases["courtid"] = row[2]
    cases["clusterid"] = row[0]

    date = row[4].split("/", 2)
    print(date)
    cases["year"] = int(date[1])

    os.chdir(sys.argv[2])
    # zipfiles = glob('*zip')

    for zfname in range(cases["year"], cases["year"] + 5):

        zfile = ZipFile(str(zfname) + ".zip")
        # year = zfname.split('/')[-1][:-4]

        print(zfname)
        members = zfile.namelist()

        for files in members:

            if fname.endswith('-maj.txt'):
                continue

            text = zfile.open(files).read().decode('utf-8')

            print(text)
            # link(text,cases["name"])
    i += 1

    if i > 10:
        break
