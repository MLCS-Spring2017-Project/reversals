import os
import pandas as pd

fields = ['caseid', 'partyWinning']

caselevel = pd.read_csv("./../../BLCircuitALL_SC_Merged.csv", skipinitialspace=True, usecols=fields)

caselevel_dict = {k: v for k, v in zip(caselevel['caseid'], caselevel['partyWinning'])}

path = "./../../datafile/text"
train_path = './../../datalabel/train'
test_path =  './../../datalabel/test/'
for root, dirs, files in os.walk(path):
    d = root.split('/')
    if d[-1] == 'text':
        continue
    if int(d[-1]) < 2000:
        for file in files:
            if file.endswith('.txt'):
                caseid = file.replace(".txt", "")
                filename = file.replace(".txt", ".lab")
                with open(os.path.join(root,file), "r") as f:
                    text = f.read()
                    with open(os.path.join(train_path, file), "w") as t:
                        t.write(text)
                with open(os.path.join(train_path, filename), 'w') as f:
                    if caselevel_dict[caseid] == 0:
                        status = 'Affirmed'
                    else:
                        status = 'Reversed'
                    f.write(status)
    else:
        for file in files:
            if file.endswith('.txt'):
                caseid = file.replace(".txt", "")
                filename = file.replace(".txt", ".lab")
                with open(os.path.join(root,file), "r") as f:
                    text = f.read()
                    with open(os.path.join(test_path, file), "w") as t:
                        t.write(text)
                with open(os.path.join(test_path, filename), 'w') as f:
                    if caselevel_dict[caseid] == 0:
                        status = 'Affirmed'
                    else:
                        status = 'Reversed'
                    f.write(status)

