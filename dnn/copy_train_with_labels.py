"""
Author: Amanpreet Singh
Description:  Creates train folder with labels for use with Magpie from already existing  train text without label files. Used for district to circuit
Usage: `python dnn/copy_train_with_labels dir_train dir_dnn_train`
"""

import sys
import os
import pickle
import glob


def main():
    affirm_reverse_path = os.path.abspath("district_affirm_reverse.pkl")
    dic = pickle.load(open(affirm_reverse_path, "rb"))
    curr = os.getcwd()
    os.chdir(sys.argv[1])
    files = glob.glob("./**/*.txt")
    dnn_folder = sys.argv[2]
    if not os.path.exists(dnn_folder):
        os.makedirs(dnn_folder)

    for fname in files:
        docid = fname.split('/')[-1][:-4]
        case = dic.loc[dic['caseid'] == docid]
        status = check_case_status(case)

        if not status:
            continue

        # circuit = fname.split('/')[1]
        # dnn_folder_circuit = os.path.join(dnn_folder, circuit)
        # if not os.path.exists(dnn_folder_circuit):
        #     os.makedirs(dnn_folder_circuit)

        train_text_file = os.path.join(dnn_folder, docid + ".txt")
        train_text_label = os.path.join(dnn_folder, docid + ".lab")
        if os.path.exists(train_text_file):
            raise Exception("File already exists")

        with open(fname, "r") as f:
            text = f.read()
            with open(train_text_file, "w") as t:
                t.write(text)

        with open(train_text_label, "w") as f:
            f.write(status)


def check_case_status(case):
    if case.empty:
        return False
    elif case['Affirmed'].tolist()[0] == 0.0 \
            and case['Reversed'].tolist()[0] == 0.0:
        return False
    elif case['Affirmed'].tolist()[0] == 1.0:
        status = "Affirmed"
    else:
        status = "Reversed"
    return status


if __name__ == "__main__":
    main()
