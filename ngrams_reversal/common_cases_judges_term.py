import pandas as pd
import os
import csv
import sys
from collections import defaultdict
import pickle


def count_judges(j1_party, j2_party, j3_party):
    num_judges_party1 = 0
    num_judges_party2 = 0
    num_judges_party_other = 0

    try:
        if int(j1_party) == 0:
            num_judges_party1 += 5
        elif int(j1_party) == 1:
            num_judges_party2 += 5
        else:
            num_judges_party_other += 5
    except ValueError:
        num_judges_party_other += 5

    try:
        if int(j2_party) == 0:
            num_judges_party1 += 5
        elif int(j2_party) == 1:
            num_judges_party2 += 5
        else:
            num_judges_party_other += 5
    except ValueError:
        num_judges_party_other += 5

    try:
        if int(j3_party) == 0:
            num_judges_party1 += 5
        elif int(j3_party) == 1:
            num_judges_party2 += 5
        else:
            num_judges_party_other += 5
    except ValueError:
        num_judges_party_other += 5

    return num_judges_party1, num_judges_party2, num_judges_party_other

def create_data():

    fields = ['caseid', 'partyWinning', 'j1party', 'j2party', 'j3party']
    caselevel = pd.read_csv("./../../BLCircuitALL_SC_Merged.csv", skipinitialspace=True, usecols=fields)
    caselevel_dict = {k: v for k, v in zip(caselevel['caseid'], caselevel['partyWinning'])}
    caselevel_dict_judges = {}
    for case_id, j1_party, j2_party, j3_party in zip(caselevel['caseid'], caselevel['j1party'], caselevel['j2party'], caselevel['j3party']):
        num_judges_party1, num_judges_party2, num_judges_party_other = count_judges(j1_party, j2_party, j3_party)
        caselevel_dict_judges[case_id] = (num_judges_party1, num_judges_party2, num_judges_party_other)
    x_train = []
    y_train = []
    x_test = []
    y_test = []
    total_cases = 0
    path = "./../../data"
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
                num_judges_party1, num_judges_party2, num_judges_party_other = caselevel_dict_judges[caseid]
                dictionary['num_judges_party1'] = num_judges_party1
                dictionary['num_judges_party2'] = num_judges_party2
                dictionary['num_judges_party_other'] = num_judges_party_other
                x_train.append(dictionary)
                y_train.append(caselevel_dict[caseid])
            for i in range(train_len, total_len):
                caseid = files[i].replace(".txt", "")
                print(caseid)
                with open(os.path.join(root, files[i]), mode='rb') as infile:
                    dictionary = pickle.load(infile)
                num_judges_party1, num_judges_party2, num_judges_party_other = caselevel_dict_judges[caseid]
                dictionary['num_judges_party1'] = num_judges_party1
                dictionary['num_judges_party2'] = num_judges_party2
                dictionary['num_judges_party_other'] = num_judges_party_other
                x_test.append(dictionary)
                y_test.append(caselevel_dict[caseid])
    print(total_cases)
    with open('./../../x_train_judges_term.pickle', 'wb') as handle:
        pickle.dump(x_train, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('./../../y_train_judges_term.pickle', 'wb') as handle:
        pickle.dump(y_train, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('./../../x_test_judges_term.pickle', 'wb') as handle:
        pickle.dump(x_test, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('./../../y_test_judges_term.pickle', 'wb') as handle:
        pickle.dump(y_test, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    create_data()

