#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-25 20:29:52
# @Author  : luckcul (tyfdream@gmail.com)
# @Version : 2.7.12

from svm import *

def loadDataSet(fileName) :
	data = []
	label = []
	f = file(fileName, 'r')
	for line in f.readlines():
		x = line.strip().split('\t')
		data.append(map(float, x[:-1]))
		label.append(float(x[-1]))
	return data, label

def plotData(data, label, alphas, b):
	'''
	show two dimension
	'''
	plt.figure(1)
	L = len(data)
	# plot data
	for i in range(L):
		plt.plot(data[i][0], data[i][1], 'go' if label[i] == 1 else 'bo')
	svPoint = np.nonzero(alphas.A)[0]
	for i in svPoint:
		# ii = int(i)
		plt.plot(data[i][0], data[i][1], 'r^' if label[i] == 1 else 'r^')
	# cal hyper plane
	t = np.arange(-1.5, 10, 0.01)
	w = calWs(data, label, alphas)
	print w
	# print w
	for i in svPoint:
		# print i, 
		dis = w * np.mat(data[i]).T  +b 
		# print dis * label[i]
	tt = (-w[0, 0]*t -b)/w[0, 1]
	tt = tt.A1
	plt.plot(t, tt)
	plt.show()

def testLinearSVM():
	'''
	test linear svm with soft margin	
	'''
	data, label = loadDataSet('testSet.txt')
	Svm = trainSVM(data[0:80], label[0:80], 0.6, 0.0001, 1000)
	testSVM(Svm, data[80:], label[80:])
	plotData(data[0:80], label[0:80], Svm.alphas, Svm.b)

def testRbfSVM(args = 1):
	'''
	test non-linear svm (rbf-kernel)
	'''
	data, label = loadDataSet('testSetRBF.txt')
	Svm = trainSVM(data, label, 211, 0.0001, 10000, ('rbf', args))
	data, label = loadDataSet('testSetRBF2.txt')
	testSVM(Svm, data, label)

if __name__ == '__main__':
	testLinearSVM()
	testRbfSVM()