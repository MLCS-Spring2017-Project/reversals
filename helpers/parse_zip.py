import os
import pickle
import collections

from glob import glob
from zipfile import ZipFile


def parse(dir, generator):

    os.chdir(dir)
    zipfiles = glob('*zip')
    for zfname in zipfiles:

        print(zfname)
        zfile = ZipFile(zfname)    
        year = zfname.split('/')[-1][:-4]
        members = zfile.namelist()        
        
        threshold = len(members) / 200
        dic = pickle.load(open("affirm_reverse.pkl", "rb"))    
        docfreqs = []        
        
        for fname in members:
            
            # "maj" means this is the majority opinion
            if not fname.endswith('-maj.txt'):
                continue

            docid = fname.split('/')[-1][:-4]

            if dic.loc[dic['caseid'] == docid]['Affirmed'].tolist()[0] == 0.0 && dic.loc[dic['caseid'] == docid]['Reversed'].tolist()[0] == 0.0:
                continue
            elif dic.loc[dic['caseid'] == docid]['Affirmed'].tolist()[0] == 1.0:
                status = "Affirmed"
            else:
                status = "Reversed"

            text = zfile.open(fname).read().decode()
            tup = (generator(text),status)
            docfreqs.append(tup)

        pickle.dump(docfreqs, open(zfname + ".pkl","wb"))
