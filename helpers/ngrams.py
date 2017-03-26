import nltk
import string
import pickle
import os

from helpers import utils
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from nltk.corpus import stopwords
from collections import Counter
from nltk import CFG


grammar_string = """
  S -> TWO | THREE | FOUR

  TWO -> A N | N N | V N | V V | N V | V P
  THREE -> N N N | A A N | A N N | N A N | N P N | V A N | V N N | A V N | V V N | V P N | A N V | N V V | V D N | V V V | N N V | V V P | V A V | V V N | N C N | V C V | A C A | P A N
  FOUR -> N C V N | A N N N | N N N N | N P N N | A A N N | A N N N | A N P N | N N P N | N P A N | A C A N | N C N N | N N C N | A N C N | N C A N | P D A N | P N P N | V D N N | V D A N | V V D N

  A -> 'JJ' | 'JJR' | 'JJS'
  N -> 'NN' | 'NNS' | 'NNP' | 'NNPS' | 'PRP' | 'PRP$'
  V -> 'VB' | 'VBD' | 'VBG' | 'VBN' | 'VBP' | 'VBZ' | 'RB' | 'RBR' | 'RBS' | 'WRB'
  P -> 'IN'
  C -> 'CC' | 'CD'
  D -> 'DT' | 'PDT' | 'WDT'

  M -> '.' """

grammar = CFG.fromstring(grammar_string)

terminals = {'JJ': None, 'JJR': None, 'JJS': None, 'NN': None, 'NNS': None, 'NNP': None, 'NNPS': None, 'PRP': None,
             'PRP$': None, 'VB': None, 'VBD': None, 'VBG': None, 'VBN': None, 'VBP': None, 'VBZ': None, 'RB': None,
             'RBR': None, 'RBS': None, 'WRB': None, 'IN': None, 'CC': None, 'CD': None, 'DT': None, 'PDT': None,
             'WDT': None}


class NgramGenerator:
    def __init__(self, N=5):
        self.stopset = set(stopwords.words('english'))
        self.N = N
        self.affirm_reverse_path = os.path.abspath("affirm_reverse.pkl")
        self.dic = pickle.load(open(self.affirm_reverse_path, "rb"))
        return

    def get_sentences(self, case_data):
        """
        Returns a list of sentences from a string of possibly many sentences
        """

        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

        return tokenizer.tokenize(case_data)

    def parse(self, text):
        """
        Checks if the provided text has a valid parse
        """

        parser = nltk.ChartParser(grammar)
        tree = parser.parse(text)

        valid_parse = False

        for t in tree:
            valid_parse = True
            break

        return valid_parse

    def generate(self, txt):
        """
        Processes a directory containing a set of case documents and generates
        n-grams. The n-grams thus generated shall be
        stored in {data_dir}/n-grams/
        """

        # Read the case data from the string
        case_data = txt

        valid_n_grams = {}

        # Go over every sentence in the document
        for sentence in self.get_sentences(case_data):

            pos_tuples = nltk.pos_tag(nltk.word_tokenize(sentence))

            # Update the grammar if required and get the POS tags
            pos_tags = self.get_pos_tags(pos_tuples)

            # Generate N-Grams of tags
            n_grams = []
            for n in range(1, self.N + 1):
                n_grams.extend([list(grams)
                                for grams in ngrams(
                                range(len(pos_tuples)), n)])

            # Get only the n-grams that match the defined grammar
            for i in range(len(n_grams)):

                # Generate n-gram list and check validity
                if self.parse([pos_tags[j] for j in n_grams[i]]):

                    # Append words to overall list
                    elements = ' '.join([pos_tuples[k][0] for k in n_grams[i]])

                    if elements in valid_n_grams:
                        valid_n_grams[elements] += 1
                    else:
                        valid_n_grams[elements] = 1

        return valid_n_grams

    def get_pos_tags(self, pos_tuples):
        """
        Returns the POS tags from POS tuples of (word, tag)
        Updates the grammar for unknown tags
        """

        global grammar_string
        global grammar
        global terminals

        changed_grammar = False
        pos_tags = []

        for pos_tuple in pos_tuples:
            tag = pos_tuple[1]

            if tag not in terminals:

                if tag == '\'\'':
                    tag = 'APOS'

                grammar_string += ' | \'' + tag + '\''

                terminals[tag] = None
                changed_grammar = True

            pos_tags.append(tag)

        if changed_grammar:
            grammar = CFG.fromstring(grammar_string)

        return pos_tags

    def generate_ngram_txts(self, zfile, zfname, dir):
        year = zfname.split('/')[-1][:-4]
        members = zfile.namelist()

        threshold = 0
        feature_points = []
        # docfreqs = {
        #     "affirmed": Counter(),
        #     "reversed": Counter()
        # }

        for fname in members:

            # "maj" means this is the majority opinion
            if not fname.endswith('-maj.txt'):
                continue

            docid = fname.split('/')[-1][:-8]
            case = self.dic.loc[self.dic['caseid'] == docid]
            if case.empty:
                continue
            elif case['Affirmed'].tolist()[0] == 0.0 \
                    and case['Reversed'].tolist()[0] == 0.0:
                continue
            elif case['Affirmed'].tolist()[0] == 1.0:
                status = "Affirmed"
            else:
                status = "Reversed"

            threshold += 1
            text = zfile.open(fname).read().decode('utf-8')
            ngrams = self.generate(text)
            # lower_status = status.lower()

            # for gram in ngrams:
            #     docfreqs[lower_status][gram] += 1

            tup = (ngrams, status)
            utils.save_dict_to_file(dir + "/" + year + "/" + docid, ngrams)

        # threshold = float(threshold) / 200
        # affirmed_counter = Counter()
        # for gram in list(docfreqs["affirmed"]):
        #     if docfreqs["affirmed"][gram] > threshold:
        #         affirmed_counter[gram] = docfreqs["affirmed"][gram]
        #
        # docfreqs["affirmed"] = affirmed_counter
        #
        # reversed_counter = Counter()
        # for gram in list(docfreqs["reversed"]):
        #     if docfreqs["reversed"][gram] > threshold:
        #         reversed_counter[gram] = docfreqs["reversed"][gram]
        #
        # docfreqs["reversed"] = reversed_counter
        #
        # for i in range(len(feature_points)):
        #     tup = feature_points[i]
        #     lower_status = tup[1].lower()
        #
        #     counter = Counter()
        #     for gram in tup[0]:
        #         if gram in docfreqs[lower_status]:
        #             counter[gram] = tup[0][gram]
        #     feature_points[i] = (counter, tup[1])
