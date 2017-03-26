import pickle

if __name__ == '__main__':
    dic = pickle.load(open("data/1880-ngrams.pkl", "rb"))
    print(dic[0:])
