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

    if int(j1_party) == 0:
        num_judges_party1 += 1
    elif int(j1_party) == 1:
        num_judges_party2 += 1
    else:
        num_judges_party_other += 1

    if int(j2_party) == 0:
        num_judges_party1 += 1
    elif int(j2_party) == 1:
        num_judges_party2 += 1
    else:
        num_judges_party_other += 1

    if int(j3_party) == 0:
        num_judges_party1 += 1
    elif int(j3_party) == 1:
        num_judges_party2 += 1
    else:
        num_judges_party_other += 1

    return num_judges_party1, num_judges_party2, num_judges_party_other


def create_data():

    fields = ['caseid', 'partyWinning', 'j1party', 'j2party', 'j3party']

    caselevel = pd.read_csv("./../../BLCircuitALL_SC_Merged.csv", skipinitialspace=True, usecols=fields)

    caselevel_dict = {k: v for k, v in zip(caselevel['caseid'], caselevel['partyWinning'])}
    caselevel_dict_judges = {}

    for case_id, j1_party, j2_party, j3_party in zip(caselevel['caseid'], caselevel['j1party'], caselevel['j2party'], caselevel['j3party']):
        num_judges_party1, num_judges_party2, num_judges_party_other = count_judges(j1_party, j2_party, j3_party)
        caselevel_dict_judges[caseid] = (num_judges_party1, num_judges_party2, num_judges_party_other)

    # caselevel_set = set(caselevel['blcaseid'])

    path = "./../../data"

    dictionary = defaultdict(int)

    x_data = []

    y_data = []

    i = 0
    for root, dirs, files in os.walk(path):
        for name in files:

            if name.endswith((".txt")):
                caseid = name.replace(".txt", "")
            print(caseid)
            if caseid in caselevel_dict:
                i += 1
                with open(os.path.join(root, name), mode='r') as infile:
                    reader = csv.reader(infile)
                    dictionary = {rows[0]: int(rows[1]) for rows in reader}
                    dictionary['num_judges_party1'] = num_judges_party1
                    dictionary['num_judges_party2'] = num_judges_party2
                    dictionary['num_judges_party_other'] = num_judges_party_other

                x_data.append(dictionary)
                y_data.append(caselevel_dict[caseid])

    print("Number of common cases between ngrams and caselevel data : ", i)
    with open('./../../x_data.pickle', 'wb') as handle:
        pickle.dump(x_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('./../../y_data.pickle', 'wb') as handle:
        pickle.dump(y_data, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    create_data()
