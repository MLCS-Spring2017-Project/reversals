import pandas as pd
import os
import csv
import sys
from collections import defaultdict
import pickle


def count_judges(j1_party, j2_party, j3_party):
    Republicans = 0
    Democrats = 0
    Other_party = 0

    try:
        if int(j1_party) == 0:
            Republicans += 5
        elif int(j1_party) == 1:
            Democrats += 5
        else:
            Other_party += 5
    except ValueError:
        Other_party += 5

    try:
        if int(j2_party) == 0:
            Republicans += 5
        elif int(j2_party) == 1:
            Democrats += 5
        else:
            Other_party += 5
    except ValueError:
        Other_party += 5

    try:
        if int(j3_party) == 0:
            Republicans += 5
        elif int(j3_party) == 1:
            Democrats += 5
        else:
            Other_party += 5
    except ValueError:
        Other_party += 5

    return Republicans, Democrats, Other_party

def create_data():

    fields = ['caseid', 'partyWinning', 'j1party', 'j2party', 'j3party']
    caselevel = pd.read_csv("./../../BLCircuitALL_SC_Merged.csv", skipinitialspace=True, usecols=fields)
    caselevel_dict = {k: v for k, v in zip(caselevel['caseid'], caselevel['partyWinning'])}
    caselevel_dict_judges = {}
    for case_id, j1_party, j2_party, j3_party in zip(caselevel['caseid'], caselevel['j1party'], caselevel['j2party'], caselevel['j3party']):
        Republicans, Democrats, Other_party = count_judges(j1_party, j2_party, j3_party)
        caselevel_dict_judges[case_id] = (Republicans, Democrats, Other_party)
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
                # print(caseid)
                with open(os.path.join(root, files[i]), mode='rb') as infile:
                    dictionary = pickle.load(infile)
                Republicans, Democrats, Other_party = caselevel_dict_judges[caseid]
                dictionary['Republicans'] = Republicans
                dictionary['Democrats'] = Democrats
                dictionary['Other_party'] = Other_party
                try:
                    if int(j1_party) == 0:
                        dictionary['j1_republican'] = 1
                        dictionary['j1_democrat'] = 0
                        dictionary['j1_other'] = 0
                    elif int(j1_party) == 1:
                        dictionary['j1_republican'] = 0
                        dictionary['j1_democrat'] = 1
                        dictionary['j1_other'] = 0
                    else:
                        dictionary['j1_republican'] = 0
                        dictionary['j1_democrat'] = 0
                        dictionary['j1_other'] = 1
                except:
                    pass
                try:
                    if int(j2_party) == 0:
                        dictionary['j2_republican'] = 1
                        dictionary['j2_democrat'] = 0
                        dictionary['j2_other'] = 0
                    elif int(j2_party) == 1:
                        dictionary['j2_republican'] = 0
                        dictionary['j2_democrat'] = 1
                        dictionary['j2_other'] = 0
                    else:
                        dictionary['j2_republican'] = 0
                        dictionary['j2_democrat'] = 0
                        dictionary['j2_other'] = 1
                except:
                    pass
                try:
                    if int(j3_party) == 0:
                        dictionary['j3_republican'] = 1
                        dictionary['j3_democrat'] = 0
                        dictionary['j3_other'] = 0
                    elif int(j3_party) == 1:
                        dictionary['j3_republican'] = 0
                        dictionary['j3_democrat'] = 1
                        dictionary['j3_other'] = 0
                    else:
                        dictionary['j3_republican'] = 0
                        dictionary['j3_democrat'] = 0
                        dictionary['j3_other'] = 1
                except:
                    pass

                x_train.append(dictionary)
                y_train.append(caselevel_dict[caseid])
            for i in range(train_len, total_len):
                caseid = files[i].replace(".txt", "")
                # print(caseid)
                with open(os.path.join(root, files[i]), mode='rb') as infile:
                    dictionary = pickle.load(infile)
                Republicans, Democrats, Other_party = caselevel_dict_judges[caseid]
                dictionary['Republicans'] = Republicans
                dictionary['Democrats'] = Democrats
                dictionary['Other_party'] = Other_party
                try:
                    if int(j1_party) == 0:
                        dictionary['j1_republican'] = 1
                        dictionary['j1_democrat'] = 0
                        dictionary['j1_other'] = 0
                    elif int(j1_party) == 1:
                        dictionary['j1_republican'] = 0
                        dictionary['j1_democrat'] = 1
                        dictionary['j1_other'] = 0
                    else:
                        dictionary['j1_republican'] = 0
                        dictionary['j1_democrat'] = 0
                        dictionary['j1_other'] = 1
                except:
                    pass
                try:
                    if int(j2_party) == 0:
                        dictionary['j2_republican'] = 1
                        dictionary['j2_democrat'] = 0
                        dictionary['j2_other'] = 0
                    elif int(j2_party) == 1:
                        dictionary['j2_republican'] = 0
                        dictionary['j2_democrat'] = 1
                        dictionary['j2_other'] = 0
                    else:
                        dictionary['j2_republican'] = 0
                        dictionary['j2_democrat'] = 0
                        dictionary['j2_other'] = 1
                except:
                    pass
                try:
                    if int(j3_party) == 0:
                        dictionary['j3_republican'] = 1
                        dictionary['j3_democrat'] = 0
                        dictionary['j3_other'] = 0
                    elif int(j3_party) == 1:
                        dictionary['j3_republican'] = 0
                        dictionary['j3_democrat'] = 1
                        dictionary['j3_other'] = 0
                    else:
                        dictionary['j3_republican'] = 0
                        dictionary['j3_democrat'] = 0
                        dictionary['j3_other'] = 1
                except:
                    pass
                x_test.append(dictionary)
                y_test.append(caselevel_dict[caseid])
    print(total_cases)
    with open('./../../x_train_features_term.pickle', 'wb') as handle:
        pickle.dump(x_train, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('./../../y_train_features_term.pickle', 'wb') as handle:
        pickle.dump(y_train, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('./../../x_test_features_term.pickle', 'wb') as handle:
        pickle.dump(x_test, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('./../../y_test_features_term.pickle', 'wb') as handle:
        pickle.dump(y_test, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    create_data()

