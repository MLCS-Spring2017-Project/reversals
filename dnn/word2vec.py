"""
File for training word2vec model on a corpus
Usage: `python word2vec.py corpus_path save_path`

Save_path is where the model will be saved
"""

import gensim
import logging
import sys
import os
import glob
from zipfile import ZipFile


class FileIterator(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in glob.glob(self.dirname, recursive=True):
            for line in open(fname):
                yield line.split()


class ZipIterator(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for zfname in glob.glob(self.dirname, recursive=True):
            zfile = ZipFile(zfname)
            members = zfile.namelist()
            for fname in members:
                if not fname.endswith('-maj.txt'):
                    continue
                data = zfile.read(fname).decode()
                yield data.split()


def main():
    save_path = os.path.join(sys.argv[2], "word2vec.model")
    path = sys.argv[1]

    if len(sys.argv) > 3:
        path = os.path.join(path, "**", "*.zip")
        files = ZipIterator(path)
    else:
        path = os.path.join(path, "**", "*.txt")

        files = FileIterator(path)

    if os.path.exists(save_path):
        model = gensim.models.Word2Vec.load(save_path)
        model.train(files)
    else:
        model = gensim.models.Word2Vec(files, min_count=15, iter=50, workers=4)

    model.save(save_path)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    main()
