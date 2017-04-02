import csv
import sys
import os
import pickle
import argparse

from collections import Counter
from glob import glob
from zipfile import ZipFile
from difflib import SequenceMatcher
from helpers.circuit_parser import CircuitParser


class Mapper:
    def __init__(self, args):
        self.link = dict()
        self.args = args
        self.similarity_score = 0.9
        self.pickle_folder = os.path.abspath(self.args.pickle_folder)

        with open(self.args.dccsv, newline='') as file:

            self.entry = csv.reader(file)

            for row in self.entry:

                if row[1] not in self.link:
                    self.link[row[1]] = []

                if row[0] not in self.link[row[1]]:
                    self.link[row[1]].append(row[0])

    def run(self):
        self.parser = CircuitParser()

        with open(self.args.district_sorted, newline='') as csv_file:
            self.csv_file = csv_file

            self.entry = csv.reader(self.csv_file)
            os.chdir(self.args.circuit_data)
            zipfiles = glob('*zip')
            zipfiles = sorted(zipfiles)

            for zfname in zipfiles:

                print(zfname)
                self.link_year(zfname)

    def link_year(self, zfname):
        year = int(zfname.split('/')[-1][:-4])

        if year < self.args.year:
            return

        found = dict()
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

                                    if docid not in found:
                                        found[docid] = []

                                    found[docid].append(row[0] + "/" +
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

                                    if docid not in found:
                                        found[docid] = []

                                    found[docid].append(row[0] + "/" +
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

        path = "%s/%s_%s.pkl" % (self.pickle_folder, year, self.similarity_score)
        with open(path, 'wb') as handle:
            pickle.dump(found, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="District to Circuit Linker")
    parser.add_argument("dccsv", type=str, action="store",
                        help="District to Circuit Link csv")
    parser.add_argument("circuit_data", type=str, action="store",
                        help="Folder which contains yearwise circuit data")
    parser.add_argument("district_sorted", type=str, action="store",
                        help="Year wise sorted csv")
    parser.add_argument("pickle_folder", type=str, action="store", default=".",
                        help="Folder in which pickles will be stored")
    parser.add_argument("--year", "-y", type=int, action="store", default=1924,
                        help="Year from where to start linking")
    args = parser.parse_args()
    mapper = Mapper(args)
    mapper.run()
