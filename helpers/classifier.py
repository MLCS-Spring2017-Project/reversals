from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import BernoulliNB
from glob import glob

from helpers import utils
import os
import pickle


class Classifier:
    def __init__(self):
        self.classifier = SklearnClassifier(BernoulliNB())
        self.affirm_reverse_path = os.path.abspath("affirm_reverse.pkl")
        self.dic = pickle.load(open(self.affirm_reverse_path, "rb"))

    def fetch(self, dir):
        os.chdir(dir)
        files = glob("./**/*.txt")

        datapoints = []
        for fname in files:
            docid = fname.split('/')[-1][:-4]
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

            dic = utils.read_file_to_dict(fname)
            datapoints.append((dic, status))
        return datapoints

    def train(self, train_data):
        self.classifier.train(train_data)

    def perdict(self, test_data):
        return self.classifier.classify(test_data)
