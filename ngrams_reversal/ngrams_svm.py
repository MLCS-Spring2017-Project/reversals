

# class review_instance:
# """ Build the review class """
# 	def __init__(self):
# 		self.word_list = []
# 		self.label = 0
# 		self.word_dict = Counter()
# 		self.word_tfidf = Counter()

# 	def set_label(self, label_val):
# 		self.label = label_val

# 	def read_file(self, file_name):
		
# 		#Read each file into a list of strings. And set the list to self.word_list
		
# 		f = open(file_name)
# 		lines = f.read().split(’ ’)
# 		symbols = '${}()[].,:;+-*/&|<=>~" '
# 		words = map(lambda Element: Element.translate(None, symbols).strip(), lines)
# 		words = filter(None, words)
# 		self.word_list = words
# 		self.construct_word_dict(stop_word=stopwords.words(’english’))

# 	def construct_word_dict(self, stop_word=None, count_words=None):
# 		"""
# 		count the words in word_list, transform to a dict of (word: word_count)
# 		:param stop_word: a list of stop words, The words you hope to filter, not
# 		included in dict, default set to None
# 		:param count_words: a list, the words you hope to keep in the count_dict, if
# 		set to None, will keep all the words
# 		:return:
# 		"""
# 		c = Counter()
# 		c = Counter(self.word_list)
# 		if count_words:
# 			c = Counter({i: c[i] for i in count_words})

# 		if stop_word:
# 			for i in stop_word:
# 				del c[i]
# 		seld.word_dict = c
# 	def transform_to_tfidf(self, idf_dict):
# 	"""
# 	Take a idf dict as input, constrcut the {word: tfidf} vector tfidf = tf
# 	*
# 	(idf
# 	+1)
# 	"""
# 		for word in self.word_dict:
# 			self.word_tfidf[word] = self.word_dict.get(word)*idf_dict.get(word, 1)

# import ast

# def reading(self):

# 	path = "/home/karthik/Documents/COURT"
#     with open('deed.txt', 'r') as f:
#         s = f.read()
#         self.whip = ast.literal_eval(s)

import pandas as pd
import os

# def make_training_data ():
# 	fields = ['caseid']
# 	caselevel = pd.read_csv("/home/karthik/Documents/COURT/BloombergCASELEVEL_Touse.csv",skipinitialspace=True, usecols=fields)

# 	caselevel_set = set(caselevel)


# 	for root, dirs, files in os.walk(path):
# 		for name in files:
# 			if name.endswith((".txt")):
# 				name.replace(".txt","")
# 			if name in caselevel_set:
# 				print(name)

          


def pegasos_fast(review_list, max_epoch, lam, watch_list=None, tfidf= False):
"""
A faster version of pegasos tfidf: whether use tfidf features
"""
	if lam < 0:
		sys.exit("Lam must be greater than 0")
	print "lambda = %r, use tfidf = %r" %(lam, tfidf)
	#Initialization
	weight = Counter()
	epoch = 0
	t = 1.
	review_number = len(review_list)
	s = 1.
	while epoch < max_epoch:
		start_time = time.time()
		epoch += 1
		for j in xrange(review_number):
			t += 1
			eta = 1./(t*lam)
			s = (1 -eta*lam)*s
			review = review_list[j]
			label = review.label
			if tfidf:
				feature = review.word_tfidf
			else:
				feature = review.word_dict
			if label*dotProduct(feature, weight) < 1:
				temp = eta*	label/s
				increment(weight, temp, feature)
				#print weight
		end_time = time.time()
		epoch_weight = Counter()
		increment(epoch_weight, s, weight)
		print "Epoch %r: in %.3f seconds. Training accuracy: %.3f, Test accuracy:%.3f" %(epoch, end_time-start_time, accuracy_percent(review_list, epoch_weight
		, tfidf=tfidf) accuracy_percent(watch_list, epoch_weight, tfidf=tfidf))
	return epoch_weight


def svm_predict(review_X, weight):
	if dotProduct(weight, review_X)>0:
		return 1
	else:
		return -1
def accuracy_percent(review_list, weight, tfidf=False):
	label_list = [i.label for i in review_list]
	if tfidf:
		predict_list = [svm_predict(i.word_tfidf, weight) for i in review_list]
	else:
		predict_list = [svm_predict(i.word_dict, weight) for i in review_list]
		return sum([1 for i in range(len(label_list)) if label_list[i] == predict_list[i]]) /float(len(label_list))