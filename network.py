import pandas as pd
import numpy as np
import re
import csv
from math import log
from decimal import Decimal
from ast import literal_eval
from pattern.en import singularize, pluralize

## futher cleaning (part of ingredients were manually selected/removed)
nodeDF = pd.read_csv("/Users/Jiajia/Google Drive/Columbia/Big Data/MyNodes copy.csv", header=None, names=['ingredients'])
units_pl = ['heads', 'fluid', 'optional', 'slices', 'jars', 'other', '']
units = ['head', 'fluid', 'optional', 'slice', 'jar']
for i in range(nodeDF.count()):
	nodeDF.ingredients.iloc[i] = re.sub('^(%s)' % '|'.join(units_pl), '', nodeDF.ingredients.iloc[i])
	nodeDF.ingredients.iloc[i] = re.sub('(%s)$' % '|'.join(units_pl), '', nodeDF.ingredients.iloc[i])
	nodeDF.ingredients.iloc[i] = re.sub('^(%s)' % '|'.join(units), '', nodeDF.ingredients.iloc[i])
	nodeDF.ingredients.iloc[i] = re.sub('(%s)$' % '|'.join(units), '', nodeDF.ingredients.iloc[i])  
	nodeDF.ingredients.iloc[i] = re.sub('\s{2,}', ' ', nodeDF.ingredients.iloc[i]).strip(' ')	
	#print ing

## all words to sigular
for i in range(nodeDF.count()):
	nodeDF.ingredients.iloc[i] = singularize(nodeDF.ingredients.iloc[i])
	nodeDF.ingredients.iloc[i] = re.sub('olife', 'olive', nodeDF.ingredients.iloc[i])
	nodeDF.ingredients.iloc[i] = re.sub('flmy', 'flour', nodeDF.ingredients.iloc[i])
	nodeDF.ingredients.iloc[i] = re.sub('pastum', 'pasta', nodeDF.ingredients.iloc[i])
	nodeDF.ingredients.iloc[i] = re.sub('spaghettus', 'spaghetti', nodeDF.ingredients.iloc[i])
	nodeDF.ingredients.iloc[i] = re.sub('tamarus', 'tamari', nodeDF.ingredients.iloc[i])
	nodeDF.ingredients.iloc[i] = re.sub('Velveetum', 'Velveeta', nodeDF.ingredients.iloc[i])
	nodeDF.ingredients.iloc[i] = re.sub('fetum', 'feta', nodeDF.ingredients.iloc[i])
	nodeDF.ingredients.iloc[i] = re.sub('Vidalium', 'Vidalia', nodeDF.ingredients.iloc[i])

nodeDF = nodeDF.drop_duplicates()
nodeDF.index = range(nodeDF.count())

nodeDF.loc[:1959].to_csv('Clean_nodes.csv', encoding='utf8', index=True, header=False)

recDF = pd.read_csv("/Users/Jiajia/Google Drive/Columbia/Big Data/Clean_recipe.csv", header=None, names=['ingredients'])
for i in range(recDF.count()):
	recDF.ingredients.iloc[i] = re.sub(',ange\s', ',orange ', recDF.ingredients.iloc[i])
	recDF.ingredients.iloc[i] = re.sub(',ange,', ',orange,', recDF.ingredients.iloc[i])
	recDF.ingredients.iloc[i] = re.sub(',ange-', ',orange-', recDF.ingredients.iloc[i])
	recDF.ingredients.iloc[i] = re.sub(',anges', ',oranges', recDF.ingredients.iloc[i])
	recDF.ingredients.iloc[i] = re.sub(',anges,', ',oranges,', recDF.ingredients.iloc[i])
	recDF.ingredients.iloc[i] = re.sub(',egano\s', ',oregano ', recDF.ingredients.iloc[i])

recDF.to_csv('Clean_recipes.csv', encoding='utf8', index=True, header=False)

nodeDF = pd.read_csv("/Users/Jiajia/Google Drive/Columbia/Big Data/Clean_nodes.csv", header=None, names=['ingredients'])
recDF = pd.read_csv("/Users/Jiajia/Google Drive/Columbia/Big Data/Clean_recipes.csv", header=None, names=['ingredients'])
n = nodeDF.count()['ingredients']    ## n = 1960
m = recDF.count()['ingredients']
prob_ingr = np.zeros(n)


## Compute probability of each ingredient
nodeDF['ingredients'] = nodeDF['ingredients'].str.lower()
recDF['ingredients'] = recDF['ingredients'].str.lower()

location = []
for i, ingr in nodeDF.iterrows():
	count = 0
	occur = []
	for r, recp in recDF.iterrows():
		if ingr['ingredients'] in recp['ingredients'] or (pluralize(ingr['ingredients']) in recp['ingredients']):
			count += 1
			occur.append(r)
	if count == 0:
		print i, ingr
	else:
		prob_ingr[i] = count*1.0 / m
		location.append(occur)

with open('prob.csv', 'wb') as myfile:
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	for prob in prob_ingr:
		wr.writerow([prob])

with open('location.csv', 'wb') as myfile:
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	for loc in location:
		wr.writerow([loc])


## Compute PMI and Generate Edges
position = []
with open('/Users/Jiajia/Google Drive/Columbia/Big Data/location.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:       # each row is read as a list
    	position.append(literal_eval(row[0]))

prob = []
with open('/Users/Jiajia/Google Drive/Columbia/Big Data/prob.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
    	prob.append(Decimal(row[0]))

PMI = np.empty([n, n])
edges = []
for i in range(n-1):
	for j in range(i+1,n):
		common = len(set(position[i]) & set(position[j]))
		jointprob = Decimal(common) / Decimal(m)
		if jointprob != 0:
			PMI[i][j] = log(jointprob/(prob[i] * prob[j]))
			PMI[j][i] = PMI[i][j]
			if PMI[i][j] > 0.05:		#threshold
				edges.append({'source':i, 'target':j})
for k in range(n):
	PMI[k][k] = -log(prob[k])

np.save('PMImatrix.npy', PMI)

edgeDF = pd.DataFrame(edges)
edgeDF.to_csv('Edges.csv', index=False, header=False)




