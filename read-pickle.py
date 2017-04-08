import pickle

if __name__ == '__main__':
    dic = pickle.load(open("../Data/district_affirm_reverse.pkl", "rb"))
    print(dic)
