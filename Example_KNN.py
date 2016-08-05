# -*- coding: utf-8 -*-
'''
@ nahumst
KNN

See more: 
https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm
https://en.wikipedia.org/wiki/Iris_flower_data_set

'''

from scipy.spatial import distance
from collections import Counter
import numpy as np

def euclidean(a, b):
	return distance.euclidean(a, b)

def majority_vote(classes): # ArgMax 
	value, count = Counter(classes).most_common()[0]
	return value

class KNN(object):
	'''docstring for KNN'''
	def __init__(self, k = 1):
		super(KNN, self).__init__()
		self.k = k
	
	def fit(self, X_train, y_train):
		self.X_train = X_train
		self.y_train = y_train

	def predict(self, X_test):
		predictions = []
		for x_test in X_test:
			labels = []
			X_train = self.X_train[:]
			y_train = self.y_train[:]	
			for i in xrange(self.k):
				best_index = self.closest(X_train, x_test)				
				labels.append(y_train[best_index])
				X_train = np.delete(X_train, best_index, 0)
				y_train = np.delete(y_train, best_index, 0)
			predictions.append(majority_vote(labels))	

		return predictions

	def closest(self, X_data, x_row):
		best_distance = euclidean(X_data[0], x_row)
		best_index = 0
		for x_index in xrange(1, len(X_data)):
			distance = euclidean(X_data[x_index], x_row)
			if distance < best_distance:
				best_distance = distance
				best_index = x_index
		return best_index


from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier 
iris = load_iris()
print iris.DESCR

X = iris.data
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .25)

knn_1 = KNN(k = 3)
knn_1.fit(X_train, y_train)
predictions = knn_1.predict(X_test)
print 'My Knn       {predict} % accuracy'.format(predict = accuracy_score(y_test, predictions))

knn_2 = KNeighborsClassifier(n_neighbors = 3)
knn_2.fit(X_train, y_train)
predictions = knn_2.predict(X_test)
print 'Sklearn Knn  {predict} % accuracy'.format(predict = accuracy_score(y_test, predictions))




