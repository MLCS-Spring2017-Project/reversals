from nltk.classify import SklearnClassifier
from nltk import compat
from sklearn.naive_bayes import MultinomialNB
from glob import glob
from sklearn.externals import joblib
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.preprocessing import LabelEncoder

from helpers import utils
import os
import pickle

CLASSIFIER_PICKLE_PATH = "partial_classifier.pkl"


class PartialClassifier:
    def __init__(self):
        self.classifier = MultinomialNB()
        self.affirm_reverse_path = os.path.abspath("district_affirm_reverse.pkl")
        self.dic = pickle.load(open(self.affirm_reverse_path, "rb"))
        self.first_call = False
        self.encoder = LabelEncoder()
        self.vectorizer = HashingVectorizer(charset="latin-1")

    def fetch(self, dir):
        curr_dir = os.getcwd()
        os.chdir(dir)
        files = glob("./**/*.txt")

        datasets = []
        for fname in files:
            # print(fname)
            docid = fname.split('/')[-1][:-4]
            case = self.dic.loc[self.dic['caseid'] == docid]
            status = self.check_case_status(case)
            if not status:
                continue

            text = utils.text_from_district_file(fname)
            datasets.append((text, status))
        os.chdir(curr_dir)
        return datasets

    def check_case_status(self, case):
        if case.empty:
            return False
        elif case['Affirmed'].tolist()[0] == 0.0 \
                and case['Reversed'].tolist()[0] == 0.0:
            return False
        elif case['Affirmed'].tolist()[0] == 1.0:
            status = "Affirmed"
        else:
            status = "Reversed"
        return status

    def train(self, train_data):
        X, y = list(compat.izip(*train_data))
        X = self.vectorizer.transform(X)
        y = self.encoder.fit_transform(y)

        if self.first_call:
            self.classifier.partial_fit(X, y, classes=[0, 1])
        else:
            self.classifier.partial_fit(X, y)

    def save_classifier(self):
        dump = {
            'classifier': self.classifier,
            'encoder': self.encoder,
            'vectorizer': self.vectorizer
        }

        joblib.dump(dump, CLASSIFIER_PICKLE_PATH)

    def load_classifier(self):
        if os.path.exists(CLASSIFIER_PICKLE_PATH):
            dump = joblib.load(CLASSIFIER_PICKLE_PATH)
            self.encoder = dump['encoder']
            self.classifier = dump['classifier']
            self.vectorizer = dump['vectorizer']
        else:
            self.first_call = True

    def predict(self, dir):
        curr_dir = os.getcwd()
        os.chdir(dir)
        files = glob("./**/*.txt")

        datapoints = []
        classes = self.encoder.classes_
        validation_target = []
        validation_data = []
        for fname in files:
            docid = fname.split('/')[-1][:-4]
            case = self.dic.loc[self.dic['caseid'] == docid]
            status = self.check_case_status(case)
            validation_data.append(utils.text_from_district_file(fname))
            validation_target.append(status)

        X = self.vectorizer.transform(validation_data)
        y = self.encoder.transform(y)
        score = clf.score(X_validation, target_validation)

        print(score)
        os.chdir(curr_dir)
