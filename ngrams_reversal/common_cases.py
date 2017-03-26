import pandas as pd
import os
import csv
import sys
from collections import defaultdict
import pickle


def create_data():

    fields = ['caseid', 'Reversed']

    caselevel = pd.read_csv("./../../BloombergCASELEVEL_Touse.csv", skipinitialspace=True, usecols=fields)

    caselevel_dict = {k: v for k, v in zip(caselevel['caseid'], caselevel['Reversed'])}

    caselevel_set = set(caselevel['caseid'])

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
                    dictionary = {rows[0]: rows[1] for rows in reader}

                x_data.append(dictionary)
                y_data.append(caselevel_dict[caseid])

    print("Number of common cases between ngrams and caselevel data : ", i)
    with open('./../../x_data.pickle', 'wb') as handle:
        pickle.dump(x_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('./../../y_data.pickle', 'wb') as handle:
        pickle.dump(y_data, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    create_data()
