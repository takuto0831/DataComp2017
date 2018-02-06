# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 17:21:21 2017

@author: SHIO-160412-4
"""
import numpy as np
import scipy as sc
from scipy import linalg
from scipy import spatial
import scipy.spatial.distance
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager
import pylab

dataset = data.iloc[:,8:14]
ROW = dataset.shape[0]
COL  = dataset.shape[1]

# row:行,column:列,ave:平均,vcm:分散共分散行列
row = []
column = []
ave = [0.0 for i in range(ROW)]
vcm = np.zeros((COL, ROW))
diff = np.zeros((1, ROW))
mahal = np.zeros(COL)
tmp = np.zeros(ROW)

print(dataset)

# rowにtrans_dataの要素をリストの形式で連結
for i in range(ROW):
    row.append(list(dataset.ix[i]))
print(row)

# 列を連結
for i in range(1, COL+1):
    column.append(list(dataset.ix[:, i]))
print(column)