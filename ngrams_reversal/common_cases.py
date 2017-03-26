import pandas as pd
import os
import csv
import sys
from collections import defaultdict

def create_data():

	fields = ['caseid','Reversed']


	# with open("/home/karthik/Documents/COURT/BloombergCASELEVEL_Touse.csv", mode='r') as infile:
	# 	caselevel = csv.reader(infile)
	# 	caselevel = list(row[i] for i in fields)
	# 	caselevel_dict = {case[0]:case[1] for case in caselevel}

	caselevel = pd.read_csv("/home/karthik/Documents/COURT/BloombergCASELEVEL_Touse.csv",skipinitialspace=True, usecols=fields)

	#print caselevel

	i=0

	#caselevel_dict = {case[0]:case[1] for case in caselevel}
	
	#print caselevel_dict

	caselevel_set = set(caselevel['caseid'])

	path = "/home/karthik/Documents/COURT/Ngrams/data"

	dictionary = defaultdict(int)

	data = []
	

	for root, dirs, files in os.walk(path):
		#print root,dirs,files
		for name in files:
			
			if name.endswith((".txt")):
				caseid = name.replace(".txt","")
			
			if caseid in caselevel_set:
				i+=1
				with open(os.path.join(root,name), mode='r') as infile:
					reader = csv.reader(infile)
					dictionary = {rows[0]:rows[1] for rows in reader}
				data.append(dictionary)
				
	print "Number of common cases between ngrams and caselevel data : ",i

	print data[0]

# Need to create training data with the matched cases ie "ngram for each case", "Reversed/Not"

if __name__ == '__main__':
	create_data()