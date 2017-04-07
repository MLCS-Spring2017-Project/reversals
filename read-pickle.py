import pickle

if __name__ == '__main__':
    dic = pickle.load(open("./new_pickle.pkl", "rb"))
    print(dic[0:])
