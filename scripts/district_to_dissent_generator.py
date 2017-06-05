"""
Script for matching district cases to their dissent outcome in circuit court

Usage: python district_to_dissent_generator.py "path_to_dissenterconcurrernames.csv" "path_to_unique_district_matches_pkl" "path_to_circuit_to_district_matches_pickle_folder" <optional_arg_for_saving_dict_with_folder_names>

"""
import pickle
import pandas as pd
import sys
import os

if __name__ == '__main__':

    result = dict()
    flag = 0
    dissent_df = pd.read_csv(sys.argv[1])
    dissent = {0: 0, 1: 0}
    dist_matches = pickle.load(open(sys.argv[2], "rb"))

    save_with_folder = sys.argv[4]

    for index, row in dist_matches.iterrows():
        flag = 0
        fname = os.path.join(sys.argv[3], str(row['year']) + "_95.pkl")

        try:
            circ_matches = pickle.load(open(fname, "rb"))

        except Exception:
            continue

        for circ_case, dist_case in circ_matches.items():

            for case in dist_case:
                case_name = str(case).split('/')
                caseid = case_name[0]
                if save_with_folder:
                    case_name = os.path.join(case_name[1], case_name[0])
                else:
                    case_name = caseid
                if str(caseid) == str(row['caseid']):

                    flag = 1
                    target_df = dissent_df.loc[dissent_df['caseid'] == str(circ_case)]

                    for ind, val in target_df.iterrows():

                        result[case_name] = val['dissentdummy']
                        dissent[val['dissentdummy']] += 1
                        # print(case_name, result[case_name])
                        break
                    break
            if flag:
                break

    with open('dissent_matches.pkl', 'wb') as handle:
        pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print(dissent)
