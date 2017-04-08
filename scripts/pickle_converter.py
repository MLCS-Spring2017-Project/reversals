import os
import pickle
import sys
import glob
import pandas as pd


def main():

    files = glob.glob("Data/Pickles/*.pkl")
    affirm_reverse_dict = pickle.load(open("affirm_reverse.pkl", "rb"))

    # creating DataFrame
    df = pd.DataFrame(columns=["caseid", "folder", "year", "Affirmed", "AffirmedInPart", "Reversed", "ReversedInPart"])

    count = 0

    for file in files:

        with open(file, "rb") as f:

            dic = pickle.load(f)
            # getting year out of the filename which is actually a path
            year = f.name.split("_")[0].split("/")[-1]
            print(year)

            for circ_id in dic.keys():

                # returns the row in which the circ_id matches the id in the pickle
                match = affirm_reverse_dict.loc[affirm_reverse_dict['caseid'] == circ_id]

                if match.empty:
                    continue

                # splitting the district caseid from the folder in which it would be found
                path = dic[circ_id][0].split("/")
                # saving the data in new dataframe
                df.loc[count] = [path[0], path[1], str(year), match['Affirmed'].tolist()[0], match['AffirmedInPart'].tolist()[0], match['Reversed'].tolist()[0], match['ReversedInPart'].tolist()[0]]

                count += 1

    with open('new_pickle.pkl', 'wb') as handle:
            pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    main()
