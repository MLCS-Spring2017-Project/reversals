import pandas as pd
import os


fields = ['caseid']
caselevel = pd.read_csv("/home/karthik/Documents/COURT/BloombergCASELEVEL_Touse.csv",skipinitialspace=True, usecols=fields)



i=0


caselevel_set = set(caselevel['caseid'])

path = "/home/karthik/Documents/COURT/Ngrams/data"


for root, dirs, files in os.walk(path):
	for name in files:
		
		if name.endswith((".txt")):
			name = name.replace(".txt","")
		
		if name in caselevel_set:
			i+=1
			print(name)
print "Number of common cases between ngrams and caselevel data : ",i


# Need to create training data with the matched cases ie "ngram for each case", "Reversed/Not"
