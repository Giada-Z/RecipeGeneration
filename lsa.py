import pandas as pd
import numpy as np
import re
import csv
from math import log
from decimal import Decimal
from ast import literal_eval
from pattern.en import singularize, pluralize

## Feature Selection: Dimension Reduction with SVD 
PMI = np.load('PMImatrix.npy')
U, s, V = np.linalg.svd(PMI, full_matrices=False)
S = np.diag(s)
n = S.shape[0]
total = np.trace(np.linalg.matrix_power(S, 2))

# dimension reduced from n to k = 500~650 (parameter to be tuned)
k = 650   
for i in range(n-k):
	S[n-i-1][n-i-1] = 0
percent = np.trace(np.linalg.matrix_power(S,2)) / total
# k should explain at least 90% of the energy
print percent
reducedS = S[:k,:k]
reducedV = V[:k, ]
factor = np.dot(np.linalg.inv(reducedS), reducedV)

## Incorporate Network Features to the Original Dataset

occurin = []
with open('/Users/Jiajia/Google Drive/Columbia/Big Data/location.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:       # each row is read as a list
    	occurin.append(literal_eval(row[0]))

# binary feature representation
recDF = pd.read_csv("/Users/Jiajia/Google Drive/Columbia/Big Data/Clean_recipes.csv", header=None, names=['ingredients'])
m = recDF.count()['ingredients']    
ingFeature = np.zeros((m, n))
for i in range(n):
	for loc in occurin[i]:
		ingFeature[loc, i] = 1
np.save('binary.npy', ingFeature)

# reduced features: k dimensions
reducedFeature = np.transpose(np.dot(factor, np.transpose(ingFeature)))

myrecipes = pd.read_csv("/Users/Jiajia/Google Drive/Columbia/Big Data/Recipes.csv")
myrecipes = myrecipes[['made_it_count', 'rating', 'time']]

colname = ["PMIfeature" + str(i) for i in range(k)]
featureDF = pd.DataFrame(reducedFeature, columns=colname)
myrecipes = myrecipes.join(featureDF)

## Centrality features

# degree centrality
#degree = [len(i) for i in occurin]
#degree_col = pd.Series(data=degree, name='degrees')

# betweenness centrality

# communities detection

