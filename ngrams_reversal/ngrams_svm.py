import pandas as pd
import os
import pickle
from collections import Counter
import time
from tqdm import tqdm


def dotProduct(d1, d2):
    if len(d1) < len(d2):
        return dotProduct(d2, d1)
    else:
        return sum(d1.get(f, 0) * v for f, v in d2.items())


def increment(d1, scale, d2):
    for f, v in d2.items():
        d1[f] = d1.get(f, 0) + v * scale


def pegasos_fast(x, y, max_epoch, lam):
    if lam < 0:
        sys.exit("Lam must be greater than 0")
    weight = Counter()
    epoch = 0
    t = 1.0
    x_length = len(x)
    s = 1.0
    for epoch in tqdm(range(max_epoch), desc='epoch'):
        start_time = time.time()
        for j in tqdm(range(x_length), desc='iter'):
            t += 1
            eta = 1.0 / (t * lam)
            s = (1 - eta * lam) * s
            if y[j] == 0:
                label = -1
            else:
                label = 1
            feature = x[j]
            if label * dotProduct(feature, weight) < 1:
                temp = eta * label / s
                increment(weight, temp, feature)
        end_time = time.time()
        epoch_weight = Counter()
        increment(epoch_weight, s, weight)
    return epoch_weight


def svm_predict(x, weight):
    if dotProduct(weight, x) > 0:
        return 1.0
    else:
        return 0.0


def accuracy_percent(x, y, weight):
    predict_list = [svm_predict(i, weight) for i in x]
    return sum([1 for i in range(len(y)) if y[i] == predict_list[i]]) * 100 / float(len(y))


def main():
    print('Loading the dataset')
    with open('./../../x_data.pickle', 'rb') as handle:
        x_data = pickle.load(handle)
    with open('./../../y_data.pickle', 'rb') as handle:
        y_data = pickle.load(handle)
    print('Split into Training and Test data')
    x_train = x_data[:700]
    x_test = x_data[700:]
    y_train = y_data[:700]
    y_test = y_data[700:]
    print('Running SVM')
    svm_weight = pegasos_fast(x_train, y_train, 100, 0.01)
    with open('./../../svm_weight.pickle', 'wb') as handle:
        pickle.dump(svm_weight, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print('\nAccuracy: ', accuracy_percent(x_test, y_test, svm_weight))


if __name__ == '__main__':
    main()
