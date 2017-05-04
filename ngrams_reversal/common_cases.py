import pandas as pd
import os
import csv
import sys
from collections import defaultdict
import pickle


def create_data():

    fields = ['caseid', 'partyWinning']

    caselevel = pd.read_csv("./../../BLCircuitALL_SC_Merged.csv", skipinitialspace=True, usecols=fields)

    caselevel_dict = {k: v for k, v in zip(caselevel['caseid'], caselevel['partyWinning'])}

    path = "./../../data"

    x_train = []
    x_test = []
    y_train = []
    y_test = []

    i = 0
    for root, dirs, files in os.walk(path):
        d = root.split('/')
        if(d[-1] == 'data'):
            continue
        if int(d[-1]) <= 2000:
            for name in files:
                caseid = name.replace(".txt", "")
                print(caseid)
                if caseid in caselevel_dict:
                    i += 1
                    with open(os.path.join(root, name), mode='rb') as infile:
                        dictionary = pickle.load(infile)
                    x_train.append(dictionary)
                    y_train.append(caselevel_dict[caseid])
        else:
            for name in files:
                caseid = name.replace(".txt", "")
                print(caseid)
                if caseid in caselevel_dict:
                    i += 1
                    with open(os.path.join(root, name), mode='rb') as infile:
                        dictionary = pickle.load(infile)
                    x_test.append(dictionary)
                    y_test.append(caselevel_dict[caseid])


    print("Number of common cases between ngrams and caselevel data : ", i)
    with open('./../../x_train_cases.pickle', 'wb') as handle:
        pickle.dump(x_train, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('./../../y_train_cases.pickle', 'wb') as handle:
        pickle.dump(y_train, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('./../../x_test_cases.pickle', 'wb') as handle:
        pickle.dump(x_test, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('./../../y_test_cases.pickle', 'wb') as handle:
        pickle.dump(y_test, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    create_data()
