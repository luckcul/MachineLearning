#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-16 21:25:55
# @Author  : luckcul (tyfdream@gmail.com)
# @Version : 2.7.12

import matplotlib.pyplot as plt

decisionNode  = dict(boxstyle = "sawtooth", fc = "0.8")
leafNode = dict(boxstyle = "round4", fc = "0.8")
arrow_args = dict(arrowstyle = "<-")

def getNumLeaf(tree):
	'''
	get numbers of leafs : {'a': {0: 'no', 1: {'b': {0: 'no', 1: 'yes'}}}}
	'''
	numLeaf = 0
	attri = tree.keys()[0]
	innerDict = tree[attri]
	for key in innerDict.keys():
		if type(innerDict[key]).__name__ == 'dict':
			numLeaf += getNumLeaf(innerDict[key])
		else:
			numLeaf += 1
	return numLeaf

def getTreeDepth(tree):
	'''
	get the depth of tree
	'''
	depth = 0
	attri = tree.keys()[0]
	innerDict = tree[attri]
	for key in innerDict.keys():
		if type(innerDict[key]).__name__ == 'dict':
			depth = max(depth, 1 + getTreeDepth(innerDict[key]))
		else:
			depth = max(depth, 1)
	return depth

def plotNode(nodeTxt, centerpt, parentpt, nodeType):
	createPlot.ax1.annotate(nodeTxt, xy = parentpt, xycoords = 'axes fraction', xytext = centerpt, textcoords = 'axes fraction', va = 'center', ha = 'center', bbox = nodeType, arrowprops = arrow_args)

def plotMidText(currentPt, parentPt, txt):
	'''
	plot mid String between currentPt, parentPt
	'''
	createPlot.ax1.text((parentPt[0] - currentPt[0]) / 2.0 + currentPt[0], (parentPt[1] - currentPt[1]) / 2.0 + currentPt[1], txt) #, va = 'center', ha = 'center', rotation = 0) ##~

def plotTree(tree, parentPt, nodeTxt):
	'''
	tree is what we need to plot
	parentPt is the parent of this tree
	nodeTxt is the context between parent and this root
	'''
	numLeaf = getNumLeaf(tree)
	treeDepth = getTreeDepth(tree)
	attri = tree.keys()[0]
	currentPt = (plotTree.x + (numLeaf + 1.0) / 2.0 / plotTree.totalW, plotTree.y)
	plotMidText(currentPt, parentPt, nodeTxt)
	plotNode(attri, currentPt, parentPt, decisionNode)
	innerDict = tree[attri]
	plotTree.y -= 1.0 / plotTree.totalD
	for key in innerDict.keys():
		if type(innerDict[key]).__name__ == 'dict':
			plotTree(innerDict[key], currentPt, str(key))
		else:
			plotTree.x += 1.0 / plotTree.totalW
			plotNode(innerDict[key], (plotTree.x, plotTree.y), currentPt, leafNode)
			plotMidText((plotTree.x, plotTree.y), currentPt, str(key))
	plotTree.y += 1.0 / plotTree.totalD

def createPlot(tree):
	fig = plt.figure(1, facecolor = 'white')
	fig.clf()
	axprops = dict(xticks = [], yticks = []) # cancel axies
	createPlot.ax1 = plt.subplot(111, frameon = False, **axprops)
	plotTree.totalW = float(getNumLeaf(tree))
	plotTree.totalD = float(getTreeDepth(tree))
	plotTree.y = 1.0
	plotTree.x = -0.5 / plotTree.totalW
	plotTree(tree, (0.5, 1.0), '')
	plt.show()

# def createPlot1():
# 	fig = plt.figure(1, facecolor = 'white')
# 	fig.clf()
# 	createPlot.ax1 = plt.subplot(111, frameon = False)
# 	plotNode('decision node', (0.5, 0.1), (0.1, 0.5), decisionNode)
# 	plotNode('leaf node', (0.8, 0.1), (0.3, 0.8), leafNode)
# 	plt.show()
