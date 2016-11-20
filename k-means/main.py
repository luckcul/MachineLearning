#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-11-20 20:24:34
# @Author  : luckcul (tyfdream@gmail.com)
# @Version : 2.7.12
from kMeans import *

if __name__ == "__main__":
	data = loadData(r'data.txt')
	clusterAssiment, centroids = kMeans(data, 4)
	plotAnswer(data, 4, clusterAssiment, centroids)
