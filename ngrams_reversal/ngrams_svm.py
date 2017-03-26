import pandas as pd
import os
import pickle


def pegasos_fast(review_list, max_epoch, lam, watch_list=None, tfidf=False):
    if lam < 0:
        sys.exit("Lam must be greater than 0")
    print "lambda = %r, use tfidf = %r" % (lam, tfidf)
    # Initialization
    weight = Counter()
    epoch = 0
    t = 1.
    review_number = len(review_list)
    s = 1.
    while epoch < max_epoch:
        start_time = time.time()
        epoch += 1
        for j in xrange(review_number):
            t += 1
            eta = 1. / (t * lam)
            s = (1 - eta * lam) * s
            review = review_list[j]
            label = review.label
            if tfidf:
                feature = review.word_tfidf
            else:
                feature = review.word_dict
            if label * dotProduct(feature, weight) < 1:
                temp = eta * label / s
                increment(weight, temp, feature)
                # print weight
        end_time = time.time()
        epoch_weight = Counter()
        increment(epoch_weight, s, weight)
        print "Epoch %r: in %.3f seconds. Training accuracy: %.3f, Test accuracy:%.3f" % (epoch, end_time - start_time, accuracy_percent(review_list,
            epoch_weight, tfidf=tfidf) accuracy_percent(watch_list, epoch_weight, tfidf=tfidf))
    return epoch_weight


if __name__ == '__main__':
    create_data()
