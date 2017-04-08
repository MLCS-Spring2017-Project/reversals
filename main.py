import sys
import argparse
import os

from helpers import zip_parser
from helpers import ngrams
from helpers import utils
from helpers import classifier, partial_classifier


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--ngram", action="store_true")
    parser.add_argument("-g", "--ngram_dir", action="store", default=".")
    parser.add_argument("-d", "--dir", action="store", default=".")
    parser.add_argument("-t", "--train", action="store_true")
    parser.add_argument("-p", "--predict", action="store_true")
    parser.add_argument("-pa", "--partial", action="store_true")
    parser.add_argument("file", type=str, action="store", nargs="?")
    args = parser.parse_args()

    if args.ngram:
        generator = ngrams.NgramGenerator()
        generator.generate_ngram_txts(args.dir, args.ngram_dir)
        return

    if args.partial:
        classifier_instance = partial_classifier.PartialClassifier()
    else:
        classifier_instance = classifier.Classifier()

    classifier_instance.load_classifier()

    if args.train:
        datasets = classifier_instance.fetch(args.file)
        classifier_instance.train(datasets)
        classifier_instance.save_classifier()
        return

    if args.predict:
        classifier_instance.predict(args.file)
        return


if __name__ == '__main__':
    main()
