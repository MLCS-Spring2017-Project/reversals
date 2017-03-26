import os
import pickle

from collections import Counter
from glob import glob
from zipfile import ZipFile


class ZipParser():
    def __init__(self):
        self.affirm_reverse_path = os.path.abspath("affirm_reverse.pkl")
        return

    def parse(self, dir, generator):

        os.chdir(dir)
        zipfiles = glob('*zip')
        dic = pickle.load(open(self.affirm_reverse_path, "rb"))
        for zfname in zipfiles:

            print(zfname)
            zfile = ZipFile(zfname)
            year = zfname.split('/')[-1][:-4]
            members = zfile.namelist()

            threshold = 0
            feature_points = []
            docfreqs = {
                "affirmed": Counter(),
                "reversed": Counter()
            }

            for fname in members:

                # "maj" means this is the majority opinion
                if not fname.endswith('-maj.txt'):
                    continue

                docid = fname.split('/')[-1][:-8]
                case = dic.loc[dic['caseid'] == docid]
                if case.empty:
                    continue
                elif case['Affirmed'].tolist()[0] == 0.0 \
                        and case['Reversed'].tolist()[0] == 0.0:
                    continue
                elif case['Affirmed'].tolist()[0] == 1.0:
                    status = "Affirmed"
                else:
                    status = "Reversed"

                threshold += 1
                text = zfile.open(fname).read().decode()
                ngrams = generator(text)
                lower_status = status.lower()

                for gram in ngrams:
                    docfreqs[lower_status][gram] += 1

                tup = (ngrams, status)
                feature_points.append(tup)

            threshold = float(threshold) / 200
            affirmed_counter = Counter()
            for gram in list(docfreqs["affirmed"]):
                if docfreqs["affirmed"][gram] > threshold:
                    affirmed_counter[gram] = docfreqs["affirmed"][gram]

            docfreqs["affirmed"] = affirmed_counter

            reversed_counter = Counter()
            for gram in list(docfreqs["reversed"]):
                if docfreqs["reversed"][gram] > threshold:
                    reversed_counter[gram] = docfreqs["reversed"][gram]

            docfreqs["reversed"] = reversed_counter

            for i in range(len(feature_points)):
                tup = feature_points[i]
                lower_status = tup[1].lower()

                counter = Counter()
                for gram in tup[0]:
                    if gram in docfreqs[lower_status]:
                        counter[gram] = tup[0][gram]
                feature_points[i] = (counter, tup[1])

            pickle.dump(feature_points, open(year + "-ngrams.pkl", "wb"))
            pickle.dump(docfreqs, open(year + "-docfreqs.pkl", "wb"))
