#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-19 21:26:23
# @Author  : luckcul (tyfdream@gmail.com)
# @Version : 2.7.12
from decisionTree import *
from plotTree import *

def loadLensesData():
	f = open('lenses.txt')
	dataSet = [line.strip().split('\t') for line in f.readlines()]
	labels = ['age', 'prescript', 'astigmatic', 'trarRate']
	return dataSet, labels
def main():
	# dataSet, labels = createDataSet()
	dataSet, labels = loadLensesData()
	labels_ = list(labels)
	decisionTree = createTree(dataSet, labels)

	createPlot(decisionTree)

if __name__ == '__main__':
	main()
