from helpers import ngrams
from helpers import zip_parser
import sys

if __name__ == '__main__':
    generator = ngrams.NgramGenerator()
    parser = zip_parser.ZipParser()

    parser.parse(sys.argv[1], generator.generate)
