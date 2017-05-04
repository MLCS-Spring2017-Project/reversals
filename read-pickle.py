import pickle

if __name__ == '__main__':
    dic = pickle.load(open("../Data/Pickles/1924_95.pkl", "rb"))
    print(dic)
