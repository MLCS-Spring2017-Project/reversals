from helpers import pickle_generator
from helpers import ngrams


def zip_ngram_docq_helper(zfile, zfname):
    generator = ngrams.NgramGenerator()
    pickle_gen_instance = pickle_generator.PickleGenerator()

    pickle_gen_instance.generate_ngram_docfq_pkl(
        zfile, zfname, generator.generate)
