import pickle
import numpy as np
from pathlib import Path
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestClassifier


def main():
    print('Loading the dataset')
    with open('./../../x_data.pickle', 'rb') as handle:
        x_data = pickle.load(handle)
    with open('./../../y_data.pickle', 'rb') as handle:
        y_data = pickle.load(handle)

    print('using DictVectorizer to vectorize the sparse data')
    v = DictVectorizer(sparse=False)
    x_data_vectorized = v.fit_transform(x_data)
    print('dictVectorising complete')

    print('Split into Training and Test data')
    x_train = x_data_vectorized[:1500]
    x_test = x_data_vectorized[1500:]
    y_train = y_data[:1500]
    y_test = y_data[1500:]

    print('started learing')
    clf = RandomForestClassifier(n_jobs=2)
    clf.fit(x_train, y_train)
    print('learning complete')

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
