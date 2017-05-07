from nltk.classify import SklearnClassifier
from nltk import compat
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from glob import glob
from sklearn.externals import joblib
from sklearn.feature_extraction import text
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import RandomOverSampler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from helpers import utils

import os
import pickle

CLASSIFIER_PICKLE_PATH = "partial_classifier.pkl"

court_stopwords = [
    "plaintiff",
    "plaintiffs",
    "appellee",
    "appellees",
    "appellant",
    "appellants",
    "defendant"
    "defendants",
    "petitioner"
]

stopwords = text.ENGLISH_STOP_WORDS.union(court_stopwords)


class PartialClassifier:
    def __init__(self):
        global CLASSIFIER_PICKLE_PATH
        self.classifier = RandomForestClassifier()
        CLASSIFIER_PICKLE_PATH = \
            self.classifier.__class__.__name__ + "_" + CLASSIFIER_PICKLE_PATH

        self.affirm_reverse_path = os.path.abspath("district_affirm_reverse.pkl")
        self.dic = pickle.load(open(self.affirm_reverse_path, "rb"))
        self.first_call = False
        self.encoder = LabelEncoder()
        self.tfidf = text.TfidfTransformer()
        # self.hashing_vectorizer = text.HashingVectorizer(analyzer="word", ngram_range=(1, 2), stop_words=stopwords, non_negative=True)
        self.hashing_vectorizer = text.CountVectorizer(max_features=1000)
        self.discriminant_analyzer = LinearDiscriminantAnalysis()

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
        X = self.hashing_vectorizer.fit_transform(X)
        y = self.encoder.fit_transform(y)
        X = self.tfidf.fit_transform(X)
        X = self.discriminant_analyzer.fit_transform(X.toarray(), y)

        ros = RandomOverSampler(random_state=42)
        X_res, y_res = ros.fit_sample(X, y)

        if self.first_call:
            self.classifier.fit(X_res, y_res)
        else:
            self.classifier.fit(X_res, y_res)

    def save_classifier(self):
        dump = {
            'classifier': self.classifier,
            'encoder': self.encoder,
            'hashing_vectorizer': self.hashing_vectorizer,
            'tfidf': self.tfidf
        }

        joblib.dump(dump, CLASSIFIER_PICKLE_PATH)

    def load_classifier(self):
        if os.path.exists(CLASSIFIER_PICKLE_PATH):
            dump = joblib.load(CLASSIFIER_PICKLE_PATH)
            self.encoder = dump['encoder']
            self.classifier = dump['classifier']
            self.hashing_vectorizer = dump['hashing_vectorizer']
            self.tfidf = dump['tfidf']
        else:
            self.first_call = True

    def predict(self, dir):
        curr_dir = os.getcwd()
        os.chdir(dir)
        files = glob("./**/*.txt")

        datapoints = []
        classes = self.encoder.classes_
        count = 0
        total = 0
        y = []
        predicted = []
        for fname in files:
            docid = fname.split('/')[-1][:-4]
            case = self.dic.loc[self.dic['caseid'] == docid]
            status = self.check_case_status(case)
            if not status:
                continue

            X = utils.text_from_district_file(fname)
            datapoints.append(X)
            y.append(self.encoder.transform([status])[0])

        datapoints = self.hashing_vectorizer.transform(datapoints)
        datapoints = self.tfidf.transform(datapoints)

        predicted_status = self.classifier.predict(datapoints)

        os.chdir(curr_dir)
        fpr, tpr, thresholds = metrics.roc_curve(y, predicted_status)

        print(metrics.auc(fpr, tpr))
        print(metrics.confusion_matrix(y, predicted_status))
