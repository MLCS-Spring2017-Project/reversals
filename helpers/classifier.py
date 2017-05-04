from nltk.classify import SklearnClassifier
from nltk import compat
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from glob import glob
from sklearn.externals import joblib
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import RandomOverSampler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import metrics
from helpers import utils
from scipy.signal import resample
from random import randint
import os
import pickle
import copy

CLASSIFIER_PICKLE_PATH = "classifier.pkl"


class Classifier:
    def __init__(self, dtype=float, sparse=True):
        global CLASSIFIER_PICKLE_PATH
        self.classifier = RandomForestClassifier()
        CLASSIFIER_PICKLE_PATH = \
            self.classifier.__class__.__name__ + "_" + CLASSIFIER_PICKLE_PATH
        self.affirm_reverse_path = os.path.abspath("district_affirm_reverse.pkl")
        self.dic = pickle.load(open(self.affirm_reverse_path, "rb"))
        self.first_call = False
        self.encoder = LabelEncoder()
        self.vectorizer = DictVectorizer(dtype=dtype, sparse=sparse)
        self.discriminant_analyzer = LinearDiscriminantAnalysis()

    def fetch(self, dir):
        curr_dir = os.getcwd()
        os.chdir(dir)
        files = glob("./**/*")

        datasets = {"Affirmed": [], "Reversed": []}
        for fname in files:
            # print(fname)
            docid = fname.split('/')[-1]
            case = self.dic.loc[self.dic['caseid'] == docid]
            status = self.check_case_status(case)
            if not status:
                continue

            dic = utils.read_file_to_dict(fname)
            datasets[status].append((dic, status))
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

    def oversample(self, data):
        reverse_count = len(data["Reversed"])
        affirm_count = len(data["Affirmed"])
        print(reverse_count, affirm_count)
        if reverse_count < affirm_count:
            for i in range(0, affirm_count - reverse_count):
                rand = randint(0, reverse_count)
                data["Reversed"].append(copy.deepcopy(data["Reversed"][rand]))
        print(len(data["Reversed"]))
        return data["Affirmed"] + data["Reversed"]

    def train(self, train_data):
        train_data = self.oversample(train_data)
        X, y = list(compat.izip(*train_data))
        X = self.vectorizer.fit_transform(X)
        y = self.encoder.fit_transform(y)

        if self.first_call:
            self.classifier.fit(X, y_res)
        else:
            self.classifier.fit(X, y)

    def save_classifier(self):
        dump = {
            'classifier': self.classifier,
            'encoder': self.encoder,
            'vectorizer': self.vectorizer,
            'discriminant_analyzer': self.discriminant_analyzer
        }

        joblib.dump(dump, CLASSIFIER_PICKLE_PATH)

    def load_classifier(self):
        if os.path.exists(CLASSIFIER_PICKLE_PATH):
            dump = joblib.load(CLASSIFIER_PICKLE_PATH)
            self.encoder = dump['encoder']
            self.classifier = dump['classifier']
            self.vectorizer = dump['vectorizer']
            self.discriminant_analyzer = dump['discriminant_analyzer']
        else:
            self.first_call = True

    def predict(self, dir):
        curr_dir = os.getcwd()
        os.chdir(dir)
        files = glob("./**/*")
        print(len(files))
        datapoints = []
        classes = self.encoder.classes_
        count = 0
        total = 0
        y = []
        predicted = []
        for fname in files:
            docid = fname.split('/')[-1]
            case = self.dic.loc[self.dic['caseid'] == docid]
            status = self.check_case_status(case)
            if not status:
                continue

            X = utils.read_file_to_dict(fname)
            datapoints.append(X)
            y.append(self.encoder.transform([status])[0])

        datapoints = self.vectorizer.transform(datapoints)
        predicted_status = self.classifier.predict(datapoints)

        os.chdir(curr_dir)
        fpr, tpr, thresholds = metrics.roc_curve(y, predicted_status)

        print(metrics.auc(fpr, tpr))
        print(metrics.confusion_matrix(y, predicted_status))
