import pandas as pd
import os
import pickle


def pegasos_fast(x, y, max_epoch, lam):
    if lam < 0:
        sys.exit("Lam must be greater than 0")
    weight = Counter()
    epoch = 0
    t = 1.0
    x_length = len(x)
    s = 1.0
    while epoch < max_epoch:
        start_time = time.time()
        epoch += 1
        for j in xrange(x_length):
            t += 1
            eta = 1.0 / (t * lam)
            s = (1 - eta * lam) * s
            if y[j] == 0:
                label = -1.0
            else:
                label = 1.0
            feature = x[j]
            if label * dotProduct(feature, weight) < 1:
                temp = eta * label / s
                increment(weight, temp, feature)
        end_time = time.time()
        epoch_weight = Counter()
        increment(epoch_weight, s, weight)
    return epoch_weight


def svm_predict(X_test, weight):
    if dotProduct(weight, X_test) > 0:
        return 1
    else:
        return -1


def main():
    print('loading the dataset')
    f = open('./../../x_data.pickle', 'rb')
    x = pickle.load(f)
    f.close()
    f = open('./../../y_data.pickle', 'rb')
    y_data = pickle.load(f)
    f.close()
    print('Split into Train and Test')
    x_train = x[:1500]
    x_test = x[1500:2000]
    y_train = y_data[:1500]
    y_test = y_data[1500:2000]
    svm_weight = pegasos_fast(x_train, y_train, 1000, 0.01)
    print(svm_predict(x_test[0], svm_weight), y[0])


if __name__ == '__main__':
    main()
