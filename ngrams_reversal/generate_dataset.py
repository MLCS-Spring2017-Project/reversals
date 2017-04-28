import pickle
import pandas as pd
from collections import defaultdict
import os
import sys
import helper
import generate_ngrams
import multiprocessing
from joblib import Parallel, delayed

def get_case_data(cfile):

    case_id = None
    case_data = None


    case_id = cfile.split('/')[5]
    case_id = case_id.split('-')[0]
    

    fin = open(cfile,'rb')
    case_data = pickle.load(fin)
    # print(case_data)
    fin.close()

    #print('Completed', case_id)

    return case_data




def write_file(case_id, case_data, data_dir):
    """
    Expects a list of tuples, containing (case_id, case_data)
    Writes the {case_data} into {case_id}.txt
    All the files will be written into {data_dir} directory
    """

    helper.ensure_dir(data_dir)

  
    if (case_id is None) or (case_data is None):
        return

    f = open(os.path.join(data_dir, case_id + '.txt'), 'wb')
    case_data = (' ').join(case_data)
    #print(case_data)
    f.write(case_data.encode('utf8'))
    f.close()
    #print('done writing',case_id)


def generate_case_data_files(caseterm_dict, target_dir):

    i=0

    for caseid in caseterm_dict:
        terms = [x for x in range(caseterm_dict[caseid]-5, caseterm_dict[caseid]+1)]
        for term in terms:
            data_dir = "./../../"+str(term)
            filepath = "maj/"+str(caseid)+"-maj.p"

            if helper.is_valid_file(data_dir, filepath):
                case_data = get_case_data(os.path.join(data_dir,filepath))
                write_file(caseid, case_data, os.path.join(target_dir,str(caseterm_dict[caseid])))
                i+= 1
                break
    print(i)

def generate_dataset():

    fields = ['caseid', 'term']

    caselevel = pd.read_csv("./../../BLCircuitALL_SC_Merged.csv", skipinitialspace=True, usecols=fields)

    caseterm_dict = {k: v for k, v in zip(caselevel['caseid'], caselevel['term'])}

    base_dir = "./../../datafile"

    helper.ensure_dir(base_dir)

    target_dir1 = base_dir + '/text'

    helper.ensure_dir(target_dir1)

    # generate_case_data_files(caseterm_dict, target_dir1)

    target_dir2 = base_dir + '/ngrams'

    helper.ensure_dir(target_dir2)

    to_process = None

    num_cores = multiprocessing.cpu_count()

    Parallel(n_jobs=num_cores)(delayed(generate_ngrams.process_dir)(os.path.join(root, d), os.path.join(target_dir2, d), 2, 4, b_verbose=True, b_size=to_process) for root, dirs, files in os.walk(target_dir1) for d in dirs)




if __name__ == '__main__':
    generate_dataset()