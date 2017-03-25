#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-23 19:31:09
# @Author  : luckcul (tyfdream@gmail.com)
# @Version : 2.7.6

import numpy as np 
import matplotlib.pyplot as plt
import random

class SVMStruct:
	def __init__(self, dataM, labelM, C, toler, kernelOption):
		# print dataM
		# print labelM
		# print C
		# print toler
		# print kernelOption
		self.X = dataM
		self.label = labelM
		self.C = C 
		self.toler = toler
		self.m = np.shape(dataM)[0]
		self.alphas = np.mat(np.zeros((self.m, 1)))
		self.b = 0
		self.kernelOption  = kernelOption
		self.eCache = np.mat(np.zeros((self.m, 2)))
		self.K = np.mat(np.zeros((self.m, self.m)))
		for i in range(self.m):
			self.K[:, i] = calKernel(self.X, self.X[i, :], kernelOption)

def calKernel(X, A, kernelOption):
	m, n = np.shape(X)
	K = np.mat(np.zeros((m, 1)))
	if kernelOption[0] == 'lin':
		K = X * A.T 
	elif kernelOption[0] == 'rbf':
		sigm = kernelOption[1]
		for j in range(m):
			delta = X[j, :] - A 
			K[j] = delta * delta.T 
		K = np.exp(K / (-1*2*sigm**2))
	else :
		raise NameError("no such kernel!")
	return K 

def calEk(svm, k):
	'''
	calculate E_k = f_Xk - y_k
	'''
	fXk = float(np.multiply(svm.alphas, svm.label).T * svm.K[:, k] + svm.b )
	return fXk - float(svm.label[k])

def updateEk(svm, k):
	'''
	this function and eCache is useful ?
	'''
	Ek = calEk(svm, k)
	svm.eCache[k] = [1, Ek]

def selectSecondAlpha(svm, i, Ei):
	svm.eCache[i] = [1, Ei]
	j, Ej, maxDelta = -1, -1, 0
	validEcache = np.nonzero(svm.eCache[:, 0].A)[0]
	if len(validEcache) > 1:
		for k in validEcache:
			if k == i: continue
			Ek = calEk(svm, k)
			delta = np.abs(Ei - Ek)
			if delta >= maxDelta:
				j, Ej, maxDelta = k, Ek, delta 
	else:
		#select randomly
		j = i 
		while j == i:
			j = int(random.uniform(0, svm.m))
			# j += 1
		Ej = calEk(svm, j)
	# print j, Ej, 'is select j'
	return j, Ej

def innerLoop(svm, i):
	'''
	inner loop , find 2nd alpha and update
	'''
	# print '----------------updata ', i, ' ------------------------'
	Ei = calEk(svm, i)
	# check KKT
	# y_i * f_Xi >= 1 <==> alphas_i == 0
	# y_i * f_Xi == 1 <==> 0 < alphas_i < C
	# y_i * f_Xi <= 1 <==> alphas_i == C
	if svm.label[i] * Ei >= svm.toler and svm.alphas[i] > 0 or svm.label[i] * Ei < -svm.toler and svm.alphas[i] < svm.C :
		j, Ej = selectSecondAlpha(svm, i, Ei)
		oldAlphaI = svm.alphas[i].copy()
		oldAlphaJ = svm.alphas[j].copy()
		# cal [L, H]
		if svm.label[i] == svm.label[j] :
			# print '=',
			L = max(0, svm.alphas[i] + svm.alphas[j] - svm.C)
			H = min(svm.C, svm.alphas[i] + svm.alphas[j]) 
		else:
			# print '!',
			L = max(0, -svm.alphas[i] + svm.alphas[j])
			H = min(svm.C, svm.C - svm.alphas[i] + svm.alphas[j])
		if L == H :
			# print 'L == H continue'
			return 0
		eta = svm.K[i, i] + svm.K[j, j] - 2.0 * svm.K[i, j]
		if eta <= 0:
			# print 'eta <= 0 continue'
			return 0
		svm.alphas[j] += svm.label[j]*(Ei - Ej)/eta 
		# clip alphas_j
		svm.alphas[j] = max(svm.alphas[j], L)
		svm.alphas[j] = min(svm.alphas[j], H)
		# print svm.alphas[j]
		updateEk(svm, j)
		if np.abs(svm.alphas[j] - oldAlphaJ) < 0.000001:
			# print svm.alphas[j], oldAlphaJ, 'update small continue'
			# pass
			return 0
		svm.alphas[i] += svm.label[i] * svm.label[j] * (oldAlphaJ - svm.alphas[j])
		updateEk(svm, i)
		# print i, j, 'i & j update done'
		# update b
		b1 = -Ei - svm.label[i] * svm.K[i, i] * (svm.alphas[i] - oldAlphaI) - svm.label[j] * svm.K[i, j] * (svm.alphas[j] - oldAlphaJ) + svm.b 
		b2 = -Ej - svm.label[i] * svm.K[i, j] * (svm.alphas[i] - oldAlphaI) - svm.label[j] * svm.K[j, j] * (svm.alphas[j] - oldAlphaJ) + svm.b
		if svm.alphas[i] > 0 and svm.alphas[i] < svm.C:
			svm.b = b1
		elif svm.alphas[j] > 0 and svm.alphas[j] < svm.C:
			svm.b = b2
		else:
			svm.b = (b1 + b2) / 2.0
		return 1
	else: 
		return 0

def trainSVM(dataM, labelM, C, toler, maxIter, kernelOption = ('lin',1 )):
	'''
	SMO algorithm
	dataM : list , size m*x
	labelM : list, size 1*m
	'''
	svm = SVMStruct(np.mat(dataM), np.mat(labelM).T, C, toler, kernelOption)
	iter = 0
	changed = 0
	entireDataset = True
	while (entireDataset or changed > 0) and iter < maxIter:
		changed = 0
		iter += 1
		if entireDataset :
			for i in range(svm.m):
				changed += innerLoop(svm, i)
		else:
			noBoundSet = np.nonzero( (svm.alphas.A > 0) * (svm.alphas.A < svm.C))[0]
			for i in noBoundSet:
				changed += innerLoop(svm, i)
		# change next scan dataSet
		if entireDataset :
			entireDataset = False
		elif changed == 0:
			entireDataset = True
	print 'iter : ', iter
	return svm

def calWs(data, label, alphas):
	dataM = np.mat(data)
	labelM = np.mat(label).T
	m, n = dataM.shape
	ws = np.multiply(alphas, labelM).T * dataM
	return ws

def testSVM(svm, data, label):
	dataM = np.mat(data)
	labelM = np.mat(label).T
	m, n = dataM.shape
	# only use support vector
	supportVectorIndex = np.nonzero(svm.alphas.A)[0]
	print 'support vector number :',int(supportVectorIndex.shape[0])
	supportVectorAlphas = svm.alphas[supportVectorIndex]
	supportVectorX = svm.X[supportVectorIndex]
	supportVectorY = svm.label[supportVectorIndex]
	right = 0
	for i in range(m):
		kernelValue = calKernel(supportVectorX, dataM[i, :], svm.kernelOption)
		predictYi = np.multiply(supportVectorAlphas, supportVectorY).T * kernelValue + svm.b 
		right += 1 if predictYi * labelM[i] > 0 else 0
	print 'test accuracy is : ', 1.0*right / m