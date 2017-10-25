# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 23:09:21 2017

@author: SHIO-160412-4
"""

# 階層的クラスタリング
import scipy
import numpy
import scipy.spatial.distance as distance
from matplotlib.pyplot import show
from scipy.cluster.hierarchy import linkage, dendrogram

# 時間別来店日頻度を使ってクラスタリング
result1 = linkage(data.iloc[:,9:14], metric = 'chebyshev', method = 'average')

dendrogram(result1, p=10, truncate_mode='lastp')


dArray1 = distance.pdist(data.iloc[:,9:14], metric = 'chebyshev')
