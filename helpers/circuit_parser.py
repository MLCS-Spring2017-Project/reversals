"""
Circuit Court Parser
"""

from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import string
import os
import re

map_circuit_word_to_number = {
    "first": 1,
    "second": 2,
    "third": 3,
    "fourth": 4,
    "fifth": 5,
    "sixth": 6,
    "seventh": 7,
    "eighth": 8,
    "ninth": 9,
    "tenth": 10,
    "eleventh": 11,
    "federal": "fc",
    "district": "af"
}

court_stopwords = [
    "plaintiff",
    "plaintiffs",
    "appellee",
    "appellees",
    "appellant",
    "appellants",
    "defendant"
    "defendants",
    "petitioner"
]


class CircuitParser:
    def __init__(self):
        self.stops = stopwords.words("english")
        self.stops = set()
        self.max_around_v = 3
        self.translator = str.maketrans('', '', string.punctuation)

        return

    """
    Dic contains following keys
    """
    def parse(self, preheader, major):
        global map_circuit_word_to_number
        results = dict()

        # try:
        soup = BeautifulSoup(preheader, "html.parser")
        h2 = soup.find("h2")
        center = soup.find_all("center")
        parties = soup.find_all('div', {"align": "center"})

        if h2:
            results['case_name'] = self.format(
                ','.join(h2.text.split(',')[:-1]))
        elif parties and len(parties) >= 2:
            appellee = parties[0].text
            if "appellee" in appellee.lower() or "appellant" in appellee.lower():
                appellee = self.basic_clear(appellee)
                appellee = ' '.join(appellee.split(' ')[:-2])

                appellent = parties[1].text
                appellent = self.basic_clear(appellent)
                appellent = appellent.translate(self.translator)
                appellent = ' '.join(appellent.split(' ')[:-2])

                results['case_name'] = \
                    self.format(appellee + " v. " + appellent)
        elif parties and len(parties) == 1:
            results['case_name'] = self.format(parties[0].find('p').text)
        elif "v." in center[1].text:
            results['case_name'] = self.format(center[1].text)

        if center[0]:
            court_text = center[0].text.strip('\n. ')
            court_text = court_text.lower().split(" ")
            circuit_word = court_text[-2]
            if court_text[-1] == "circuit" and \
               circuit_word in map_circuit_word_to_number:
                results['circuit_number'] = \
                    map_circuit_word_to_number[circuit_word]
            elif "district" in court_text:
                results['circuit_number'] = court_text[-1]

        # except Exception as e:
        #     print(e)
        #     pass

        return results

    def format(self, text):
        global court_stopwords
        text = self.basic_clear(text)
        text = text.split(' ')
        filtered_words = [word for word in text
                          if word not in self.stops and len(word.strip())]
        filtered_words = [word for word in filtered_words
                          if word not in court_stopwords]
        text = ' '.join(filtered_words)
        text = text.split(' v ')

        if (len(text) == 2 and isinstance(text, list)):
            text[0] = text[0].strip()
            text[1] = text[1].strip()
            text[0] = ' '.join(text[0].split(' ')[-1 * self.max_around_v:])
            text[1] = ' '.join(text[1].split(' ')[:self.max_around_v])

        return ' v '.join(text)

    def basic_clear(self, text):
        text = text.strip().lower()
        text = text.replace('\n', ' ')
        regex = re.compile(
            r"[-]")
        text = regex.sub(" ", text)
        text = text.translate(self.translator)
        return text
