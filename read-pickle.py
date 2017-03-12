import pickle

if __name__ == '__main__':
    dic = pickle.load(open("affirm_reverse.pkl", "rb"))
    print(dic)
