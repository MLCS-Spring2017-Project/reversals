import sys
import argparse
import os

from helpers import zip_parser
from helpers import ngrams
from helpers import utils
from helpers import classifier

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--ngram", action="store_true")
    parser.add_argument("-t", "--train", action="store_true")
    parser.add_argument("-p", "--predict", action="store_true")
    parser.add_argument("file", type=str)
    args = parser.parse_args()

    if args.ngram:
        parser = zip_parser.ZipParser()
        generator = ngrams.NgramGenerator()
        parser.parse(args.file, generator.generate_ngram_txts)

    if args.train:
        classifier_instance = classifier.Classifier()
        dic = classifier_instance.fetch(args.file)
        classifier_instance.train(dic)
        classifier_instance.predict(os.path.dirname(os.path.realpath(__file__)) + "/../ngram_test")
