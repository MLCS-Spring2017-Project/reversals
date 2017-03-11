from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import BernoulliNB


class Classifier:
    def __init__(self):
        self.classifier = SklearnClassifier(BernoulliNB())

    def train(self, train_data):
        self.classifier.train(train_data)

    def perdict(self, test_data):
        return self.classifier.classify(test_data)
