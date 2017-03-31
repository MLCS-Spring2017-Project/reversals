import csv
import sys
import os
import pickle

from collections import Counter
from glob import glob
from zipfile import ZipFile
from difflib import SequenceMatcher
from helpers.circuit_parser import CircuitParser


link = dict()
similarity_score = 0.9

with open(sys.argv[1], newline='') as file:

    entry = csv.reader(file)

    for row in entry:

        if row[1] not in link:
            link[row[1]] = []

        if row[0] not in link[row[1]]:
            link[row[1]].append(row[0])

# print(link)

found = dict()
count = 0

with open(sys.argv[3], newline='') as csv_file:

    entry = csv.reader(csv_file)
    os.chdir(sys.argv[2])
    zipfiles = glob('*zip')

    for zfname in zipfiles:

        print(zfname)
        year = int(zfname.split('/')[-1][:-4])

        # if year < 1927:
        #     continue

        zfile = ZipFile(zfname)
        members = zfile.namelist()

        parser = CircuitParser()
        count += 1

        for fname in members:

            if fname.endswith('-maj.txt'):
                continue
            case_det = dict()
            docid = fname.split('/')[-1][:-15]
            text_pre = zfile.open(fname).read().decode('utf-8')

            try:
                case_det = parser.parse(text_pre)
            except Exception as e:
                continue

            if len(case_det.keys()) == 0 or 'case_name' not in case_det or 'circuit_number' not in case_det:
                continue

            case_det["circuit_number"] = str(case_det["circuit_number"])
            csv_file.seek(0)
            next(entry, None)

            for row in entry:

                date = row[4].split("/", 2)
                date[2] = int(date[2])
                row[1] = parser.format(row[1])

                if date[2] <= year:

                    if abs(year - date[2]) <= 5:
                        if case_det["circuit_number"] in link:
                            # print(link[case_det["circuit_number"]], row[2])
                            if row[2] in link[case_det["circuit_number"]]:

                                if SequenceMatcher(None, case_det["case_name"], row[1]).ratio() > similarity_score:

                                    if docid not in found:
                                        found[docid] = []

                                    found[docid].append(row[0] + "/" + row[2])
                                    print(docid, row[0], row[2], "Link")

                                else:
                                    continue
                            else:
                                continue
                        else:

                            if row[3].find(case_det["circuit_number"]) != -1:

                                if SequenceMatcher(None, case_det["case_name"], row[1]).ratio() > similarity_score:

                                    if docid not in found:
                                        found[docid] = []

                                    found[docid].append(row[0] + "/" + row[2])
                                    print(docid, row[0])

                                else:
                                    continue
                            else:
                                continue
                    else:
                        continue
                else:
                    break


with open('circuit_to_district_link_0.7.pickle', 'wb') as handle:
    pickle.dump(found, handle, protocol=pickle.HIGHEST_PROTOCOL)
