import pandas as pd
import pickle

from fuzzywuzzy import fuzz

df = pd.read_csv('../District_sorted.csv')
judges_df = pd.read_pickle('District_Judges.pkl')
match_names = dict()
matched_judge_names = pd.DataFrame().reindex_like(judges_df)

# states = {'DC': 'District of Columbia', 'NY': 'New York', 'CA': 'California', 'PA': 'Pennsylvania', 'TX': 'Texas', 'Illinois': 163, 'FL': 'Florida', 'OH': 'Ohio', 'LA': 'Louisiana', 'MI': 'Michigan', 'NJ': 'New Jersey', 'MO': 'Missouri', 'GA': 'Georgia', 'AL': 'Alabama', 'VA': 'Virginia', 'TN': 'Tennessee', 'SC': 'South Carolina', 'OK': 'Oklahoma', 'NC': 'North Carolina', 'WA': 'Washington', 'AR': 'Arkansas', 'IN': 'Indiana', 'KY': 'Kentucky', 'MA': 'Massachusetts', 'CT': 'Connecticut', 'MD': 'Maryland', 'MS': 'Mississippi', 'AZ': 'Arizona', 'WV': 'West Virginia', 'MN': 'Minnesota', 'IA': 'Iowa', 'OR': 'Oregon', 'WI': 'Wisconsin', 'CO': 'Colorado', 'NV': 'Nevada', 'KS': 34, 'DE': 33, 'NM': 28, 'RI': 28, 'NE': 27, 'ME': 24, 'UT': 24, 'VT': 24, 'NH': 23, 'MT': 23, 'PR': 20, 'SD': 18, 'ID': 18, 'ND': 17, 'WY': 15, 'HI': 15, 'AK': 14, 'VI': 1}

code_to_state = {'AK':       'Alaska',
      'AL':      'Alabama',
      'AR':      'Arkansas',
      'AZ':      'Arizona',
      'CA':      'California',
      'CO':      'Colorado',
      'CT':      'Connecticut',
      'DC':      'District of Columbia',
      'DE':      'Delaware',
      'FL':      'Florida',
      'GA':      'Georgia',
      'GU':      'Guam',
      'HI':      'Hawaii',
      'IA':      'Iowa',
      'ID':      'Idaho',
      'IL':      'Illinois',
      'IN':      'Indiana',
      'KS':      'Kansas',
      'KY':      'Kentucky',
      'LA':      'Louisiana',
      'MA':      'Massachusetts',
      'MD':      'Maryland',
      'ME':      'Maine',
      'MI':      'Michigan',
      'MN':      'Minnesota',
      'MO':      'Missouri',
      'MS':      'Mississippi',
      'MT':      'Montana',
      'NC':      'North Carolina',
      'ND':      'North Dakota',
      'NE':      'Nebraska',
      'NH':      'New Hampshire',
      'NJ':      'New Jersey',
      'NM':      'New Mexico',
      'NV':      'Nevada',
      'NY':      'New York',
      'OH':      'Ohio',
      'OK':      'Oklahoma',
      'OR':      'Oregon',
      'PA':      'Pennsylvania',
      'PR':      'Puerto Rico',
      'RI':      'Rhode Island',
      'SC':      'South Carolina',
      'SD':      'South Dakota',
      'TN':      'Tennessee',
      'TX':      'Texas',
      'UT':      'Utah',
      'VA':      'Virginia',
      'VI':      'Virgin Islands',
      'VT':      'Vermont',
      'WA':      'Washington',
      'WI':      'Wisconsin',
      'WV':      'West Virginia',
      'WY':      'Wyoming'
       '':         }

count = 0
judges_df['judgelastname'] = judges_df['judgelastname'].astype(str)
judges_df['songername'] = judges_df['songername'].astype(str)
judges_df['judgefirstname'] = judges_df['judgefirstname'].astype(str)
judges_df['judgemiddlename'] = judges_df['judgemiddlename'].astype(str)
judges_df['AppointmentDate'] = pd.to_datetime(judges_df['AppointmentDate'], format='%Y-%m-%d')
judges_df['TerminationDate'] = pd.to_datetime(judges_df['TerminationDate'], format='%Y-%m-%d')
df['date_filed'] = pd.to_datetime(df['date_filed'], format='%m/%d/%Y')


for index, row in df.iterrows():

    flag = 0
    if pd.isnull(row.judges):
        continue

    judge_name = row.judges.strip()

    if judge_name != "":

        for ind,row_j_df in judges_df.iterrows():

            match_score = 0

            if fuzz.token_sort_ratio(str(row_j_df.songername), str(judge_name)) > 95:

                count+=1
                print(count)
                # print(fuzz.token_sort_ratio(row_j_df.songername, str(judge_name)))
                match_names[row.cluster_id] = ind
                # print("\nExact Match:\n")
                # print("CSV Name: " + judge_name + "\nSongername: " + row_j_df.songername)
                break

            if fuzz.token_sort_ratio(row_j_df.judgelastname, judge_name) > 95:

                try:

                    if code_to_state[row_j_df.SeatState] in row.courtname:

                        if row_j_df.AppointmentDate:
                            if row_j_df.AppointmentDate < row.date_filed:
                                match_score += 1

                        if row_j_df.TerminationDate:
                            if row_j_df.TerminationDate > row.date_filed:
                                match_score += 1

                        if match_score == 2:

                            if flag == 0:

                                flag = 1
                                to_save_ind = ind
                                # print("\nLast name match\n")
                                # print("CSV Name: " + row.judges + "\nSongername: " + row_j_df['songername'])
                            else:
                                flag = 0
                                break

                except:
                    continue

        if flag == 1:
            count+=1
            print(count)
            match_names[row.cluster_id] = to_save_ind


with open('judge_matches.pickle', 'wb') as handle:
    pickle.dump(match_names, handle, protocol=pickle.HIGHEST_PROTOCOL)

        # if flag == 1:
        #     continue

        # matched_judge_names = judges_df.loc[(fuzz.token_sort_ratio(judges_df['judgelastname'], judge_name)) > 0.95]
        #     # df.loc[df['column_name'] != some_value]

        # # except Exception as e:

        # #     count+=1
        # #     continue

        # if matched_judge_names.empty:
        #     continue
        # # else:
        # #     print(matched_judge_names)
        # #     break
        # flag = 0

        # for i, j_rows in matched_judge_names.iterrows():

        #     match_score = 0

        #     if code_to_state[j_rows.SeatState] in row.courtname:

        #         if j_rows.AppointmentDate:
        #             if j_rows.AppointmentDate < row.date_filed:
        #                 match_score += 1

        #         if j_rows.TerminationDate:
        #             if j_rows.TerminationDate > row.date_filed:
        #                 match_score += 1

        #         if match_score == 2:

        #             if flag == 0:

        #                 flag = 1
        #                 print("\n\n")
        #                 print("CSV Name: " + row.judges + "\nSongername: " + j_rows['songername'])

        #             else:
        #                 continue



        # if len(names) > 1:
        #     count+=1
        #     print(names)
    # if ' and ' in judges.lower():
    #     continue

    # judges_df.loc[lambda df: df.A > 0, :]
    # tokens = [w.upper() for w in judges.split() if w.lower() not in blacklist]

    # if len(tokens) == 0:
    #     continue
print(count)


