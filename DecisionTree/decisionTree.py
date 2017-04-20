#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-16 13:32:16
# @Author  : luckcul (tyfdream@gmail.com)
# @Version : 2.7.12

import math

def createDataSet():
	dataSet = [[1, 1, 'yes'], [1, 1, 'yes'], [1, 0, 'no'], [0, 1, 'no'], [0, 1, 'no']]
	labels = ['a', 'b']
	return dataSet, labels

def calShannonEnt(dataSet):
	'''
	calculate Shannon Entropy
	ent = -sum{p_i * log_2_pi}
	'''
	labelCounts = {}
	Len = len(dataSet)
	for vec in dataSet:
		label_ = vec[-1]
		if labelCounts.has_key(label_) :
			labelCounts[label_] += 1
		else:
			labelCounts[label_] = 1
	shannonEnt = 0.0
	for value in labelCounts.values():
		prob = value * 1.0 / Len
		shannonEnt -= prob * math.log(prob, 2)
	return shannonEnt

def splitDataSet(dataSet, feature, val):
	'''
	split dataset according data[feature] == val
	'''
	retDataSet = []
	for vec in dataSet:
		if vec[feature] == val:
			newVec = vec[:feature]
			newVec.extend(vec[feature+1:])
			retDataSet.append(newVec)
	return retDataSet

def chooseBestFeature(dataSet):
	'''
	find the largest info gain from dataSet
	'''
	numFeatures = len(dataSet[0]) - 1
	baseEntropy = calShannonEnt(dataSet)
	bestInfoGain = 0.0
	bestFeature = -1
	Len = len(dataSet)
	for i in range(numFeatures):
		uniqueFeatures = set([x[i] for x in dataSet])
		newEntropy = 0.0
		for featureVal in uniqueFeatures:
			subDataSet = splitDataSet(dataSet, i, featureVal)
			newEntropy += 1.0 * len(subDataSet) / Len * calShannonEnt(subDataSet)
		infoGain = baseEntropy - newEntropy
		if infoGain > bestInfoGain:
			bestInfoGain = infoGain
			bestFeature = i
	return bestFeature

def getMajorityLabel(labelList):
	labelCounts = {}
	for label in labelList:
		if labelCounts.has_key(label) :
			labelCounts[label] = 0
		labelCounts += 1
	sortedLabelCounts = sorted(labelCounts.iteritems(), key = operator.itemgetter(1), reverse = True)
	return sortedLabelCounts[0][0]

def createTree(dataSet, labels):
	'''
	create decision tree( ID3 )
	'''
	labelList = [x[-1] for x in dataSet]
	if len(set(labelList)) == 1:
		return labelList[0]
	if len(dataSet[0]) == 1:
		return getMajorityLabel(labelList)
	bestFeature = chooseBestFeature(dataSet)
	bestLabel = labels[bestFeature]
	del labels[bestFeature]
	decisionTree = {bestLabel:{}}
	bestFeatureValues = set([data[bestFeature] for data in dataSet])
	for value in bestFeatureValues:
		labels_ = list(labels)
		decisionTree[bestLabel][value] = createTree(splitDataSet(dataSet, bestFeature, value), labels_)
	return decisionTree

def classify(tree, labels, testVec) :
	attri = tree.keys()[0]
	innerDict = tree[attri]
	index = labels.index(attri)
	value = testVec[index]
	subTree = innerDict[value]
	if type(subTree).__name__ == 'dict':
		return classify(subTree, labels, testVec)
	else:
		return subTree

def main():
	dataSet, labels = createDataSet()
	decisionTree = createTree(dataSet, labels)
	print decisionTree

if __name__ == '__main__':
	main()

