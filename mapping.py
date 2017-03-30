import csv
import sys
import os
import pickle

from collections import Counter
from glob import glob
from zipfile import ZipFile
from helpers import dctcc_linker

link = dict()

with open(sys.argv[1], newline='') as file:

    entry = csv.reader(file)

    for row in entry:

        if row[1] not in link:
            link[row[1]] = []

        if row[0] not in link[row[1]]:
            link[row[1]].append(row[0])

# print(link)

found = {}
count = 0
with open(sys.argv[3], newline='') as csv_file:

    os.chdir(sys.argv[2])
    zipfiles = glob('*zip')

    for zfname in zipfiles:

        print(zfname)
        year = int(zfname.split('/')[-1][:-4])

        if year < 1924:
            continue

        zfile = ZipFile(zfname)
        members = zfile.namelist()

        parser = circuit_parser()
        i = 0
        count += 1

        for fname in members:

            # "maj" means this is the majority opinion
            # if not fname.endswith('-maj.txt'):
            #     continue

            if i == 0:
                docid = fname.split('/')[-1][:-4]
                text_maj = zfile.open(fname).read().decode()
                i = 1
            else:

                text_pre = zfile.open(fname).read().decode()
                case_det = parser.parse(text_pre, text_maj)

                if !len(case_det.keys()):
                    continue

                entry = csv.reader(csv_file)

                for row in entry:

                    date = row[4].split("/", 2)
                    date[2] = int(date[2])
                    row[1] = parser.format(row[1])

                    if date[2] <= case_det["year"]:
                        if abs(case_det["year"] - date[2]) <= 5:
                            if case_det["court_id"] == row[2]:
                                if case_det["case_name"] == row[1]:
                                    found[docid] = row[0]
                                    print(docid, row[0])
                                else:
                                    continue
                            else:
                                continue
                        else:
                            continue
                    else:
                        break

                i = 0

        if count > 100:
            break

# with open(sys.argv[1], newline='') as file:

#     entry = csv.reader(file)

#     i = 0
#     cases = {}
#     print(entry)

#     os.chdir(sys.argv[2])

#     for row in entry:

#         # parties = row[1].split("v.", 1)

#         if i < 100:
#             i += 1
#             continue

#         cases["name"] = row[1]
#         print(cases["name"])
#         # cases["Second_Person"] = parties[1]
#         cases["courtid"] = row[2]
#         cases["clusterid"] = row[0]

#         date = row[4].split("-", 2)
#         cases["year"] = int(date[0])

#         if(cases["year"] > 2013)
#             continue

#         for zfname in range(cases["year"], cases["year"] + 5):

#             zfile = ZipFile(str(zfname) + ".zip")

#             print(zfile)
#             members = zfile.namelist()

#             for files in members:

#                 if files.endswith('-maj.txt'):
#                     continue

#                 text = zfile.open(files).read().decode('utf-8')

#                 linker = dctcc_linker.DCTCCLinker()
#                 if linker.link(cases["name"], text):
#                     print("Link Found")

#         i += 1

#         if i > 110:
#             break
