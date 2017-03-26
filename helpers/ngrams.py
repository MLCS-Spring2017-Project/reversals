import nltk
import string
import pickle
import os

from helpers import utils
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter


class NgramGenerator:
    def __init__(self, N=5):
        self.stopset = set(stopwords.words('english'))
        self.translator = str.maketrans('', '', string.punctuation)
        self.N = N
        self.affirm_reverse_path = os.path.abspath("affirm_reverse.pkl")
        self.dic = pickle.load(open(self.affirm_reverse_path, "rb"))
        return

    def generate(self, txt):
        counter = Counter()
        txt = txt.translate(self.translator)
        tokens = word_tokenize(str(txt))
        tokens = [w for w in tokens if w not in self.stopset]
        txt = ' '.join(tokens)
        for i in range(1, self.N + 1):
            local_counter = Counter()
            grams = nltk.ngrams(txt.lower().split(), n=i)

            for gram in grams:
                local_counter[' '.join(gram)] += 1

            counter.update(local_counter)

        return counter

    def generate_ngram_txts(self, zfile, zfname, dir):
        year = zfname.split('/')[-1][:-4]
        members = zfile.namelist()

        threshold = 0
        feature_points = []
        # docfreqs = {
        #     "affirmed": Counter(),
        #     "reversed": Counter()
        # }

        for fname in members:

            # "maj" means this is the majority opinion
            if not fname.endswith('-maj.txt'):
                continue

            docid = fname.split('/')[-1][:-8]
            case = self.dic.loc[self.dic['caseid'] == docid]
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
            ngrams = self.generate(text)
            # lower_status = status.lower()

            # for gram in ngrams:
            #     docfreqs[lower_status][gram] += 1

            tup = (ngrams, status)
            utils.save_dict_to_file(dir + "/" + year + "/" + docid, ngrams)

        # threshold = float(threshold) / 200
        # affirmed_counter = Counter()
        # for gram in list(docfreqs["affirmed"]):
        #     if docfreqs["affirmed"][gram] > threshold:
        #         affirmed_counter[gram] = docfreqs["affirmed"][gram]
        #
        # docfreqs["affirmed"] = affirmed_counter
        #
        # reversed_counter = Counter()
        # for gram in list(docfreqs["reversed"]):
        #     if docfreqs["reversed"][gram] > threshold:
        #         reversed_counter[gram] = docfreqs["reversed"][gram]
        #
        # docfreqs["reversed"] = reversed_counter
        #
        # for i in range(len(feature_points)):
        #     tup = feature_points[i]
        #     lower_status = tup[1].lower()
        #
        #     counter = Counter()
        #     for gram in tup[0]:
        #         if gram in docfreqs[lower_status]:
        #             counter[gram] = tup[0][gram]
        #     feature_points[i] = (counter, tup[1])
