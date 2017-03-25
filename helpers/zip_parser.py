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

            threshold = len(members) / 200
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

                text = zfile.open(fname).read().decode()
                ngrams = generator(text)
                docfreqs[status.lower()].update(ngrams)

                tup = (ngrams, status)
                feature_points.append(tup)

            pickle.dump(feature_points, open(year + "-ngrams.pkl", "wb"))
            pickle.dump(docfreqs, open(year + "-docfreqs.pkl", "wb"))
