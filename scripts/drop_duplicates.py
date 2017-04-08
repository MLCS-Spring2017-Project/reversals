import pandas as pd
import pickle

df3 = pickle.load(open("district_affirm_reverse.pkl", "rb"))
df4 = df3.drop_duplicates(subset='caseid', keep='last')

print(df4.shape)

with open("Unique_district_matches.pkl", 'wb') as handle:
    pickle.dump(df4, handle, protocol=pickle.HIGHEST_PROTOCOL)
