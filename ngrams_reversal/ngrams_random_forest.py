import pickle
import numpy as np
from pathlib import Path
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestClassifier


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

    print('started learing')
    clf = RandomForestClassifier(n_jobs=2)
    clf.fit(x_train, y_train)
    print('learning complete')

    print('saving vectorizer and classifier in pickle')
    random_forest_classifier = {}
    random_forest_classifier['classifier'] = clf
    random_forest_classifier['vectorizer'] = v
    with open('../../RandomForestClassifier.pkl', 'wb') as handle:
        pickle.dump(random_forest_classifier, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print('making prediction and calculating accuracy')
    y_predictions = clf.predict(x_test)

    accuracy = 0.0
    for i in range(len(y_test)):
        if y_predictions[i] == y_test[i]:
            accuracy += 1.0

    accuracy = (accuracy / len(y_test)) * 100
    print('accuracy is:')
    print(accuracy)


if __name__ == '__main__':
    main()
