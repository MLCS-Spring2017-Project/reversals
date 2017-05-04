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

issue_areas = {'1' : 'Criminal Procedure', '2' : 'Civil Rights', '3' : 'First Amendment', '4' : 'Due Process',
'5' : 'Privacy', '6' : 'Attorneys', '7' : 'Unions', '8' : 'Economic Activity', '9' : 'Judicial Power',
'10' : 'Federalism', '11' : 'Interstate Relations', '12' : 'Federal Taxation', '13' : 'Miscellaneous',
'14' : 'Private Action'}

def create_data():

    fields = ['caseid', 'partyWinning', 'j1party', 'j2party', 'j3party', 'lcDisposition', 'decisionDirection', 'issueArea']

    caselevel = pd.read_csv("./../../BLCircuitALL_SC_Merged.csv", skipinitialspace=True, usecols=fields)

    caselevel_dict = {k: v for k, v in zip(caselevel['caseid'], caselevel['partyWinning'])}
    caselevel_dict_judges = {}

    for case_id, j1_party, j2_party, j3_party, lc_disposition, decision_direction, issue_area in zip(caselevel['caseid'], caselevel['j1party'],
        caselevel['j2party'], caselevel['j3party'], caselevel['lcDisposition'], caselevel['decisionDirection'], caselevel['issueArea']):
        Republicans, Democrats, Other_party = count_judges(j1_party, j2_party, j3_party)
        caselevel_dict_judges[case_id] = (Republicans, Democrats, Other_party, j1_party, j2_party, j3_party,
            lc_disposition, decision_direction, issue_area)

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
                # print(caseid)
                i += 1
                with open(os.path.join(root, name), mode='rb') as infile:
                    dictionary = pickle.load(infile)
                Republicans, Democrats, Other_party, j1_party, j2_party, j3_party, lc_disposition, decision_direction, issue_area = caselevel_dict_judges[caseid]
                dictionary['Republicans'] = Republicans
                dictionary['Democrats'] = Democrats
                dictionary['Other_party'] = Other_party

                try:
                    if int(decision_direction) == 1:
                        dictionary['lc_conservative'] = 5
                        dictionary['lc_liberal'] = 0
                    elif int(decision_direction) == 2:
                        dictionary['lc_conservative'] = 5
                        dictionary['lc_liberal'] = 0
                    else:
                        dictionary['lc_other'] = 1
                except:
                    dictionary['lc_other'] = 1
                try:
                    if int(lc_disposition) == 2 or int(lc_disposition) == 9 or int(lc_disposition) == 12:
                        dictionary['lc_affirmed'] = 5
                        dictionary['lc_reversed']  = 0
                    else:
                        dictionary['lc_affirmed'] = 0
                        dictionary['lc_reversed']  = 5
                except:
                    dictionary['lc_affirmed'] = 0
                    dictionary['lc_reversed']  = 0

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
                    dictionary['j1_republican'] = 0
                    dictionary['j1_democrat'] = 0
                    dictionary['j1_other'] = 0
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
                    dictionary['j1_republican'] = 0
                    dictionary['j1_democrat'] = 0
                    dictionary['j1_other'] = 0
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
                    dictionary['j1_republican'] = 0
                    dictionary['j1_democrat'] = 0
                    dictionary['j1_other'] = 0


                x_train.append(dictionary)
                y_train.append(caselevel_dict[caseid])
        else:
            for name in files:
                caseid = name.replace(".txt", "")
                # print(caseid)
                i += 1
                with open(os.path.join(root, name), mode='rb') as infile:
                    dictionary = pickle.load(infile)
                Republicans, Democrats, Other_party, j1_party, j3_party, j3_party, lc_disposition, decision_direction, issue_area = caselevel_dict_judges[caseid]
                dictionary['Republicans'] = Republicans
                dictionary['Democrats'] = Democrats
                dictionary['Other_party'] = Other_party

                try:
                    if int(decision_direction) == 1:
                        dictionary['lc_conservative'] = 5
                        dictionary['lc_liberal'] = 0
                    elif int(decision_direction) == 2:
                        dictionary['lc_conservative'] = 5
                        dictionary['lc_liberal'] = 0
                    else:
                        dictionary['lc_other'] = 1
                except:
                    dictionary['lc_other'] = 1
                try:
                    if int(lc_disposition) == 2 or int(lc_disposition) == 9 or int(lc_disposition) == 12:
                        dictionary['lc_affirmed'] = 5
                        dictionary['lc_reversed']  = 0
                    else:
                        dictionary['lc_affirmed'] = 0
                        dictionary['lc_reversed']  = 5
                except:
                    dictionary['lc_affirmed'] = 0
                    dictionary['lc_reversed']  = 0


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
                    dictionary['j1_republican'] = 0
                    dictionary['j1_democrat'] = 0
                    dictionary['j1_other'] = 0
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
                    dictionary['j1_republican'] = 0
                    dictionary['j1_democrat'] = 0
                    dictionary['j1_other'] = 0
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
                    dictionary['j1_republican'] = 0
                    dictionary['j1_democrat'] = 0
                    dictionary['j1_other'] = 0
                x_test.append(dictionary)
                y_test.append(caselevel_dict[caseid])

    print("Number of common cases between ngrams and caselevel data : ", i)
    with open('./../../x_train_features.pickle', 'wb') as handle:
        pickle.dump(x_train, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('./../../y_train_features.pickle', 'wb') as handle:
        pickle.dump(y_train, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('./../../x_test_features.pickle', 'wb') as handle:
        pickle.dump(x_test, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('./../../y_test_features.pickle', 'wb') as handle:
        pickle.dump(y_test, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    create_data()
