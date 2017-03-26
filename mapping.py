import csv
import sys
import os
import pickle

from collections import Counter
from glob import glob
from zipfile import ZipFile
from helpers import dctcc_linker

with open(sys.argv[1], newline='') as file:

    entry = csv.reader(file)

    i = 0
    cases = {}
    print(entry)

    os.chdir(sys.argv[2])

    for row in entry:

        # parties = row[1].split("v.", 1)

        if i < 100:
            i += 1
            continue

        cases["name"] = row[1]
        print(cases["name"])
        # cases["Second_Person"] = parties[1]
        cases["courtid"] = row[2]
        cases["clusterid"] = row[0]

        date = row[4].split("-", 2)
        print(date)
        cases["year"] = int(date[0])

        for zfname in range(cases["year"], cases["year"] + 5):

            zfile = ZipFile(str(zfname) + ".zip")

            print(zfile)
            members = zfile.namelist()

            for files in members:

                if files.endswith('-maj.txt'):
                    continue

                text = zfile.open(files).read().decode('utf-8')

                linker = dctcc_linker.DCTCCLinker()
                if linker.link(cases["name"], text):
                    print("Link Found")

        i += 1

        if i > 110:
            break
