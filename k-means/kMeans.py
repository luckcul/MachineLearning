#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-11-20 20:16:59
# @Author  : luckcul (tyfdream@gmail.com)
# @Version : 2.7.12

from numpy import *
import matplotlib.pyplot as plt

def loadData(path):
	"""
	load data 
	the type of return is list
	"""
	dataSet = []
	file = open(path)
	for line in file.readlines():
		content = line.strip().split()
		dataSet.append(map(float, content))
	return dataSet 

def randCent(dataSet, k):
	"""
	to generate k random centroids
	type of dataSet : numpy.array
	type of k : int
	type of return : numpy.array
	"""
	m = shape(dataSet)[1] # dimension of dataset
	centroids = zeros((k, m))
	Min = [min(dataSet[:, i]) for i in range(m)]
	Max = [max(dataSet[:, i]) for i in range(m)]
	interval = array(Max) - array(Min)
	randVal = random.rand(k, m)
	centroids = randVal*interval
	centroids = centroids + array(Min)
	return centroids

def calDis(x, y):
	'''
	cal the distance of x and y
	type of x and y : numpy.array 1*m
	'''
	return sum((x-y)**2)

def kMeans(dataSet, k):
	"""
	type dataset : list
	type of k : int
	"""
	data = array(dataSet)
	n, m = shape(data)
	centroids = randCent(data, k)
	changeFlag = True
	clusterAssiment = zeros((n, 2)) # dim 1 : assiment, dim 2 : distance
	while changeFlag:
		changeFlag = False
		dis = [[calDis(data[i], centroids[j]) for j in range(k)] for i in range(n)]
		dis = array(dis)
		minID = dis.argmin(axis = 1)
		minVal = dis.min(axis = 1)
		tmp = minID - clusterAssiment[:, 0]
		tmp = int32(abs(tmp))
		changeFlag = (sum(tmp) != 0)
		clusterAssiment[:,0] = minID
		clusterAssiment[:,1] = minVal
		# updata centroid
		centroids[...] = 0.0
		count = zeros((k))
		for i in range(n):
			ID = int32(clusterAssiment[(i, 0)])
			centroids[ID, :] = centroids[ID, :] + data[i, :]
			count[ID] += 1.0
		for ID in range(k):
			centroids[ID, :] = centroids[ID, :] / count[ID]
	print centroids
	return clusterAssiment, centroids

def plotAnswer(dataSet, k, clusterAssiment, centroids):
	plt.figure(1)
	symbol1 = ['ro', 'bo', 'go', 'co', 'yo', 'ko', 'mo']
	symbol2 = ['rD', 'bD', 'gD', 'cD', 'yD', 'kD', 'mD']
	n = len(dataSet)
	for i in range(n) :
		cluster = int(clusterAssiment[i, 0])
		plt.plot(dataSet[i][0], dataSet[i][1], symbol1[cluster])
	for i in range(k) :
		plt.plot(centroids[i, 0],centroids[i, 1], symbol2[i], markersize = 13)
	plt.show()