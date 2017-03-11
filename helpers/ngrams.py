import nltk
from collections import Counter


class NgramGenerator:
    def __init__(self, N=5):
        self.N = N
        return

    def generate(self, txt):
        counter = Counter()

        for i in range(1, self.N + 1):
            local_counter = Counter()
            grams = nltk.ngrams(txt.split(), n=i)

            for gram in grams:
                local_counter[' '.join(gram)] += 1

            counter.update(local_counter)

        print counter
