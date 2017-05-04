import pandas as pd
import os
import csv
import sys
from collections import defaultdict
import pickle


def create_data():
    fields = ['caseid', 'partyWinning', 'term']
    caselevel = pd.read_csv("./../../BLCircuitALL_SC_Merged.csv", skipinitialspace=True, usecols=fields)
    caselevel_dict = {k: v for k, v in zip(caselevel['caseid'], caselevel['partyWinning'])}
    path = "./../../data"
    x_train = []
    y_train = []
    x_test = []
    y_test = []
    total_cases = 0
    for root, dirs, files in os.walk(path):
        total_len = len(files)
        train_len = int(0.9*total_len)
        total_cases += total_len
        if total_len:
            for i in range(train_len):
                caseid = files[i].replace(".txt", "")
                print(caseid)
                with open(os.path.join(root, files[i]), mode='rb') as infile:
                    dictionary = pickle.load(infile)
                x_train.append(dictionary)
                y_train.append(caselevel_dict[caseid])
            for i in range(train_len, total_len):
                caseid = files[i].replace(".txt", "")
                print(caseid)
                with open(os.path.join(root, files[i]), mode='rb') as infile:
                    dictionary = pickle.load(infile)
                x_test.append(dictionary)
                y_test.append(caselevel_dict[caseid])
    print(total_cases)
    with open('./../../x_train_cases_term.pickle', 'wb') as handle:
        pickle.dump(x_train, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('./../../y_train_cases_term.pickle', 'wb') as handle:
        pickle.dump(y_train, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('./../../x_test_cases_term.pickle', 'wb') as handle:
        pickle.dump(x_test, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('./../../y_test_cases_term.pickle', 'wb') as handle:
        pickle.dump(y_test, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    create_data()

