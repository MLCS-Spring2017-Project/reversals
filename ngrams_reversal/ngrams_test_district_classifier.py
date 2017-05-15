import pickle
import numpy as np
from pathlib import Path
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics


def main():
    print('Loading the dataset')
    with open('./../../x_train.pickle', 'rb') as handle:
        x_data_train = pickle.load(handle)
    with open('./../../x_test.pickle', 'rb') as handle:
        x_data_test = pickle.load(handle)
    with open('./../../y_train.pickle', 'rb') as handle:
        y_train = pickle.load(handle)
    with open('./../../y_test.pickle', 'rb') as handle:
        y_test = pickle.load(handle)
    print('load data successful')

    with open('../../GradientBoostingClassifier_classifier_best.pkl', 'rb') as handle:
        GBC = pickle.load(handle)
    gbc_classifier = GBC['classifier']
    gbc_vectoriser = GBC['vectorizer']
    print('load Gradient boosting pickle successful')

    x_test_data = gbc_vectoriser.transform(x_test)
    print('transform x_data successful')

    print('making prediction and calculating accuracy')
    y_predictions = clf.predict(x_test_data)

    print('Accuracy: ', metrics.accuracy_score(y_test, y_predictions))
    print('AUC-ROC: ', metrics.roc_auc_score(y_test, y_predictions))
    print('Confusion matrix: ', metrics.confusion_matrix(y_test, y_predictions))


if __name__ == '__main__':
    main()
