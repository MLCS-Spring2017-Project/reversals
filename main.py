import sys

from helpers import zip_parser
from helpers import ngrams
from helpers import utils

if __name__ == '__main__':
    parser = zip_parser.ZipParser()
    generator = ngrams.NgramGenerator()
    parser.parse(sys.argv[1], generator.generate_ngram_txts)
