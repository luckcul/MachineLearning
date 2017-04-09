#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-05 20:39:20
# @Author  : luckcul (tyfdream@gmail.com)
# @Version : 2.7.12
from Apriori import *
import time
if __name__ == '__main__':
	t1 = time.time()

	f = file('mushroom.dat', 'r')
	data = []
	for line in f.readlines():
		data.append(line.split())
	itemSet, supportData = apriori(data, 0.4)
	rules = generateRules(itemSet, supportData, 0.9)

	for item in itemSet[1]:
		if item.intersection('2'):
			print item
	for item in itemSet[2]:
		if item.intersection('2'):
			print item
	print 'all rules : ', len(rules)
	print 'rules leading to 2:'
	for rule in rules:
		if rule[1] == frozenset(['2']):
			print rule

	t2 = time.time()
	print 'Time: ', t2 - t1
