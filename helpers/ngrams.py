import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import string


class NgramGenerator:
    def __init__(self, N=5):
        self.stopset = set(stopwords.words('english'))
        self.N = N
        return

    def generate(self, txt):
        counter = Counter()
        txt = txt.translate(None, string.punctuation)
        tokens = word_tokenize(str(txt))
        tokens = [w for w in tokens if w not in self.stopset]
        txt = ' '.join(tokens)
        for i in range(1, self.N + 1):
            local_counter = Counter()
            grams = nltk.ngrams(txt.lower().split(), n=i)

            for gram in grams:
                local_counter[' '.join(gram)] += 1

            counter.update(local_counter)

        return counter
