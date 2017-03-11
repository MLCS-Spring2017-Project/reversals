import nltk


class NgramGenerator:
    def __init__(self, N=5):
        self.N = N
        return

    def generate(self, txt):
        grams = nltk.ngrams(txt.split(), n=self.N)
        for gram in grams:
            print ' '.join(gram)
