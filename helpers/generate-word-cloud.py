from sklearn.ensemble import RandomForestClassifier
import pickle
import numpy as np
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt

with open('../../RandomForestClassifier.pkl', 'rb') as handle:
    dump = pickle.load(handle)

classifier = dump['classifier']
vectorizer = dump['vectorizer']

importances = classifier.feature_importances_
mean = np.mean(importances)
# important_names = vectorizer.feature_names_[importances > np.mean(importances)]


feature_names = vectorizer.feature_names_
names = {}

for i in range(len(importances)):
    if importances[i] > mean:
        names[feature_names[i]] = importances[i]

# names = sorted(names, key=lambda x: x[1], reverse=True)
maincol = np.random.randint(0, 360)  # this is the "main" color

pickle.dump(names, open("../../important_ngrams.pkl", "wb"))

wordcloud = WordCloud(background_color="white", width=900, height=500, max_words=1628, relative_scaling=1, normalize_plurals=False).generate_from_frequencies(names)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
