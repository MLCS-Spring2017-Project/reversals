import sys

from helpers import zip_parser
from helpers import utils

if __name__ == '__main__':
    parser = zip_parser.ZipParser()

    parser.parse(sys.argv[1], utils.zip_ngram_docq_helper)
