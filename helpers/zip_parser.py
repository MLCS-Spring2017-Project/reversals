import os
import pickle

from glob import glob
from zipfile import ZipFile


class ZipParser():
    def __init__(self):
        return

    def parse(self, dir, func):

        os.chdir(dir)
        zipfiles = glob('*zip')
        for zfname in zipfiles:

            print(zfname)
            zfile = ZipFile(zfname)
            func(zfile, zfname, dir)
