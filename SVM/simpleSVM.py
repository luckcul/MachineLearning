#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-18 17:02:09
# @Author  : luckcul (tyfdream@gmail.com)
# @Version : 2.7.6

import numpy as np
import matplotlib.pyplot as plt
import random

def loadDataSet(fileName) :
	data = []
	label = []
	f = file(fileName, 'r')
	for line in f.readlines():
		x = line.strip().split('\t')
		data.append(map(float, x[:-1]))
		label.append(int(x[2]))
	return data, label

def plotData(data, label, alphas, b):
	'''
	show two dimension
	'''
	labelM = np.mat(label).T
	dataM = np.mat(data)
	plt.figure(1)
	L = len(data)
	for i in range(L):
		plt.plot(data[i][0], data[i][1], 'ro' if label[i] == 1 else 'bo')
	t = np.arange(-1.5, 10, 0.01)
	w = np.multiply(alphas, labelM).T * dataM
	tt = (-w[0, 0]*t -b)/w[0, 1]
	tt = tt.A1
	plt.plot(t, tt)
	plt.show()
def selectJ(m, i):
	j = i 
	while j == i:
		j = int(random.uniform(0, m)) # return float
	return j 
def simpleSMO(data, label, C, toler, maxIter):
	dataM = np.mat(data)
	labelM = np.mat(label).T
	b = 0
	iter = 0
	m, n = np.shape(dataM)
	alphas = np.mat(np.zeros((m, 1)))
	print m, n
	while iter < maxIter:
		alphaChanged = 0
		for i in range(m):
			# cal f(xi) = sum(alpha_j * label_j * x_j) * x_j' + b
			fXi = np.multiply(alphas, labelM).T*(dataM * dataM[i,:].T) + b 
			# print dataM[i,:].T.shape, (dataM*dataM[i,:].T).shape, fXi.shape
			Ei = fXi - labelM[i] 
			# check kkt 
			# print labelM[i].shape, Ei.shape, (labelM[i])*Ei.shape
			# print (labelM[i]*Ei < toler)
			# if labelM[i]*Ei < toler:
			# 	print 'ok'
			if (alphas[i] > 0 and labelM[i]*Ei > toler) or (alphas[i] < C and labelM[i]*Ei < -toler):
				# print i,
				j = selectJ(m, i)
				# print j
				fXj = np.multiply(alphas, labelM).T*(dataM * dataM[j,:].T) + b 
				Ej = fXj - labelM[j]
				oldAlphasI = alphas[i].copy()
				oldAlphasJ = alphas[j].copy()
				#cal [L, H]
				if labelM[i] == labelM[j] :
					L = max(0, alphas[i] + alphas[j] - C)
					H = min(C, alphas[i] + alphas[j])
				else:
					L = max(0, -alphas[i] + alphas[j])
					H = min(C, C - alphas[i] + alphas[j])
				# update alpha_j
				eta = dataM[i,:] * dataM[i,:].T + dataM[j,:] * dataM[j,:].T - 2*dataM[i,:]*  dataM[j,:].T
				if eta <= 0: 
					continue
				alphas[j] = alphas[j] + labelM[j]*(Ei-Ej)/eta
				alphas[j] = max(alphas[j], L)
				alphas[j] = min(alphas[j], H)
				if abs(alphas[j] - oldAlphasJ) < 0.00001 : 
					continue
				# update alpha_j
				alphas[i] += labelM[i]*labelM[j] * (oldAlphasJ - alphas[j])
				#update b
				b1 = -Ei - labelM[i] * dataM[i,:] * dataM[i,:].T * (alphas[i] - oldAlphasI) - labelM[j] * dataM[j,:] * dataM[i,:].T * (alphas[j] - oldAlphasJ) + b 
				b2 = -Ej - labelM[i] * dataM[i,:] * dataM[j,:].T * (alphas[i] - oldAlphasI) - labelM[j] * dataM[j,:] * dataM[j,:].T * (alphas[j] - oldAlphasJ) + b
				if alphas[i] > 0 and alphas[i] < C:
					b = b1
				elif alphas[j] > 0 and alphas[j] < C:
					b = b2
				else:
					b = (b1+b2) / 2
				alphaChanged += 1
		if alphaChanged == 0: iter += 1
		else: iter = 0
		# print iter,
	return alphas, b



if __name__ == '__main__':
	data, label = loadDataSet('testSet.txt')
	alphas, b = simpleSMO(data, label, 0.6, 0.001, 200)
	plotData(data, label, alphas, b)
	print alphas[alphas>0], b