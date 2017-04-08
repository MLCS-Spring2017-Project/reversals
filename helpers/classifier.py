from nltk.classify import SklearnClassifier
from nltk import compat
from sklearn.naive_bayes import MultinomialNB
from glob import glob
from sklearn.externals import joblib
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import LabelEncoder

from helpers import utils
import os
import pickle

CLASSIFIER_PICKLE_PATH = "classifier.pkl"


class Classifier:
    def __init__(self, dtype=float, sparse=True):
        self.classifier = MultinomialNB()
        self.affirm_reverse_path = os.path.abspath("district_affirm_reverse.pkl")
        self.dic = pickle.load(open(self.affirm_reverse_path, "rb"))
        self.first_call = False
        self.encoder = LabelEncoder()
        self.vectorizer = DictVectorizer(dtype=dtype, sparse=sparse)

    def fetch(self, dir):
        curr_dir = os.getcwd()
        os.chdir(dir)
        files = glob("./**/*")

        datasets = []
        for fname in files:
            # print(fname)
            docid = fname.split('/')[-1]
            case = self.dic.loc[self.dic['caseid'] == docid]
            status = self.check_case_status(case)
            if not status:
                continue

            dic = utils.read_file_to_dict(fname)
            datasets.append((dic, status))
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
        X = self.vectorizer.fit_transform(X)
        y = self.encoder.fit_transform(y)

        if self.first_call:
            self.classifier.fit(X, y, classes=[0, 1])
        else:
            self.classifier.fit(X, y)

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
        files = glob("./**/*")

        datapoints = []
        classes = self.encoder.classes_
        count = 0
        for fname in files:
            docid = fname.split('/')[-1]
            case = self.dic.loc[self.dic['caseid'] == docid]
            status = self.check_case_status(case)
            test_data = utils.read_file_to_dict(fname)
            X = self.vectorizer.transform(test_data)

            predicted_status = self.classifier.predict(X)

            count += status == classes[predicted_status][0]

        os.chdir(curr_dir)
        print(float(count) / len(files))
