#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-29 22:28:05
# @Author  : luckcul (tyfdream@gmail.com)
# @Version : 2.7.12

def loadData():
	return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

def generateItem(dataSet) :
	'''
	generate one-size item set
	'''
	ret = []
	for data in dataSet:
		for x in data:
			if [x] not in ret:
				ret.append([x])
	ret.sort() # neccesary ?
	return map(frozenset, ret) # using frozenset for dict hash.

def checkSupport(dataSet, ck, minSupport = 0.5) :
	'''
	dataSet is list of set
	check items in ck >= minSupport
	'''
	support = {}
	for data in dataSet:
		for itemSet in  ck:
			if itemSet.issubset(data):
				if support.has_key(itemSet):
					support[itemSet] += 1
				else :
					support[itemSet] = 1
	ret = []
	supportData = {}
	Len = len(dataSet)
	for si in support:
		supportV = 1.0 * support[si] / Len
		if supportV >= minSupport:
			ret.append(si)
			supportData[si] = supportV # add items that >= minSupport
	return ret, supportData



def generateNextC(Lk, k):
	'''
	length k -> length k+1
	'''
	# print Lk, '..'
	Len = len(Lk)
	ret = []
	for i in range(Len):
		for j in range(i+1, Len):
			L1 = list(Lk[i])
			L2 = list(Lk[j])
			L1.sort()
			L2.sort()
			if L1[:k-2] == L2[:k-2]:
				ret.append(Lk[i] | Lk[j])
	return ret

def apriori(dataSet, minSupport = 0.5):
	'''
	'''
	c1 = generateItem(dataSet)
	D = map(set, dataSet)
	L1, supportData = checkSupport(D, c1, minSupport)
	L = [L1]
	k = 2
	while True :
		Ck = generateNextC(L[k-2], k)
		Lk, supportD = checkSupport(D, Ck, minSupport)
		if len(Lk) == 0:break
		supportData.update(supportD)
		L.append(Lk)
		k += 1
	return L, supportData

#---------------FIND association rule-------------------
def generateRules(L, supportData, minSupport = 0.7):
	RuleList = []
	for i in range(1, len(L)): # start with len of 2
		for freqSet in L[i]:
			tmp = [frozenset([xi]) for xi in freqSet] # convert {a, b, c} to [{a}, {b}, {c}]
			calConf(freqSet, tmp, supportData, RuleList, minSupport)
			if i > 1:
				getRulesFromOneSet(freqSet, tmp, supportData, RuleList, minSupport)
	return RuleList

def calConf(freSet, rightItem, supportData, RuleList, minSupport = 0.7):
	ret = []
	for item in rightItem:
		conf = supportData[freSet] / supportData[freSet - item]
		if conf >= minSupport:
			RuleList.append((freSet - item, item, conf))
			ret.append(item)
	return ret
def getRulesFromOneSet(freSet, rightItem, supportData, RuleList, minSupport = 0.7):
	'''
	make sure len(rightItem) > 0
	'''
	m = len(rightItem[0])
	# calConf(freSet, rightItem, supportData, RuleList, minSupport)
	if len(freSet) > m+1:
		items_ = generateNextC(rightItem, m+1)
		items_ = calConf(freSet, items_, supportData, RuleList, minSupport)
		if len(items_) > 1:
			getRulesFromOneSet(freSet, items_, supportData, RuleList, minSupport)

