import pickle
import numpy as np
from pathlib import Path
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import metrics


def main():
    print('Loading the dataset')
    with open('./../../x_train_judges.pickle', 'rb') as handle:
        x_data_train = pickle.load(handle)
    with open('./../../x_test_judges.pickle', 'rb') as handle:
        x_data_test = pickle.load(handle)
    with open('./../../y_train_judges.pickle', 'rb') as handle:
        y_train = pickle.load(handle)
    with open('./../../y_test_judges.pickle', 'rb') as handle:
        y_test = pickle.load(handle)

    x_data = x_data_train + x_data_test
    len_train = len(x_data_train)
    len_test = len(x_data_test)

    print('using DictVectorizer to vectorize the sparse data')
    v = DictVectorizer(sparse=True)
    x_data_vectorized = v.fit_transform(x_data)
    print('dictVectorising complete')

    print('Split into Training and Test data')
    x_train = x_data_vectorized[:len_train]
    x_test = x_data_vectorized[len_train:]

    print('started learning')
    clf = GradientBoostingClassifier()
    clf.fit(x_train, y_train)
    print('learning complete')

    print('saving vectorizer and classifier in pickle')
    gradient_boosting_classifier = {}
    gradient_boosting_classifier['classifier'] = clf
    gradient_boosting_classifier['vectorizer'] = v
    with open('../../GradientBoostingClassifier.pkl', 'wb') as handle:
        pickle.dump(gradient_boosting_classifier, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print('making prediction and calculating accuracy')
    y_predictions = clf.predict(x_test)

    print('Accuracy: ', metrics.accuracy_score(y_test, y_predictions))
    print('AUC-ROC: ', metrics.roc_auc_score(y_test, y_predictions))
    print('Confusion matrix: ', metrics.confusion_matrix(y_test, y_predictions))


if __name__ == '__main__':
    main()
