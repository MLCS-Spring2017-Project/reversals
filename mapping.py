import csv
import sys
import os
import pickle

from collections import Counter
from glob import glob
from zipfile import ZipFile
from difflib import SequenceMatcher
from helpers.circuit_parser import CircuitParser


class Mapper:
    def __init__(self):
        self.link = dict()
        self.similarity_score = 0.9

        with open(sys.argv[1], newline='') as file:

            self.entry = csv.reader(file)

            for row in self.entry:

                if row[1] not in self.link:
                    self.link[row[1]] = []

                if row[0] not in self.link[row[1]]:
                    self.link[row[1]].append(row[0])

    def run(self):
        self.found = dict()
        self.parser = CircuitParser()

        with open(sys.argv[3], newline='') as csv_file:
            self.csv_file = csv_file

            self.entry = csv.reader(self.csv_file)
            os.chdir(sys.argv[2])
            zipfiles = glob('*zip')

            for zfname in zipfiles:

                print(zfname)
                self.link_year(zfname)

        with open('circuit_to_district_link_0.7.pickle', 'wb') as handle:
            pickle.dump(self.found, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def link_year(self, zfname):
        year = int(zfname.split('/')[-1][:-4])

        # if year < 1927:
        #     continue

        zfile = ZipFile(zfname)
        members = zfile.namelist()

        for fname in members:

            if fname.endswith('-maj.txt'):
                continue
            case_det = dict()
            docid = fname.split('/')[-1][:-15]
            text_pre = zfile.open(fname).read().decode('utf-8')

            try:
                case_det = self.parser.parse(text_pre)
            except Exception as e:
                continue

            if len(case_det.keys()) == 0 or 'case_name' not in case_det or \
               'circuit_number' not in case_det:
                continue

            case_det["circuit_number"] = str(case_det["circuit_number"])
            self.csv_file.seek(0)
            next(self.entry, None)

            for row in self.entry:

                date = row[4].split("/", 2)
                date[2] = int(date[2])
                row[1] = self.parser.format(row[1])

                if date[2] <= year:

                    if abs(year - date[2]) <= 5:
                        if case_det["circuit_number"] in self.link:
                            if row[2] in self.link[case_det["circuit_number"]]:

                                if SequenceMatcher(None, case_det["case_name"],
                                   row[1]).ratio() > self.similarity_score:

                                    if docid not in self.found:
                                        self.found[docid] = []

                                    self.found[docid].append(row[0] + "/" +
                                                             row[2])
                                    print(docid, row[0], row[2], "Link")

                                else:
                                    continue
                            else:
                                continue
                        else:

                            if row[3].find(case_det["circuit_number"]) != -1:

                                if SequenceMatcher(None, case_det["case_name"],
                                                   row[1]).ratio() > \
                                   self.similarity_score:

                                    if docid not in self.found:
                                        self.found[docid] = []

                                    self.found[docid].append(row[0] + "/" +
                                                             row[2])
                                    print(docid, row[0])

                                else:
                                    continue
                            else:
                                continue
                    else:
                        continue
                else:
                    break


if __name__ == '__main__':
    mapper = Mapper()
    mapper.run()
