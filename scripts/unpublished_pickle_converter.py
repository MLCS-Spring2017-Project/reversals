import os
import pickle
import sys
import glob
import pandas as pd


def main():

    affirm_reverse_dict = pickle.load(open("unpublished_affirm_reverse.pkl", "rb"))

    # creating DataFrame
    df = pd.DataFrame(columns=["caseid", "folder", "year", "Affirmed", "AffirmedInPart", "Reversed", "ReversedInPart"])

    count = 0
    pickles = {}

    for item, value in affirm_reverse_dict.items():
        if value[0] not in pickles:
            f = "pickles/%s_95.pkl" % value[0]
            dic = pickle.load(open(f, "rb"))
            pickles[value[0]] = dic
        else:
            dic = pickles[value[0]]
        # getting year out of the filename which is actually a path
        year = value[0]
        # splitting the district caseid from the folder in which it would be found
        path = value[1][0].split("/")
        # saving the data in new dataframe
        affirmed = value[3] == "Affirmed"
        reversed = value[3] == "Reversed"
        df.loc[count] = [path[0], path[1], str(year), afffirmed, 0, 0, reversed]

        count += 1

    with open('unique_district_affirm_reverse.pkl', 'wb') as handle:
            pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    main()
