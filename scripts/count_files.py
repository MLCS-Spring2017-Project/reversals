import os

count = 0

for folder in os.listdir("Matched_district_data"):

    for file in os.listdir("Matched_district_data/" + folder):

        count += 1

print(count)
