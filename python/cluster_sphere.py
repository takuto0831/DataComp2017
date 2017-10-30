# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 16:24:45 2017

@author: SHIO-160412-4
"""
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn import metrics

import sys
sys.path.append('C:/Users/SHIO-160412-4/Desktop/spherecluster')

from spherecluster import SphericalKMeans
from spherecluster import VonMisesFisherMixture
from spherecluster import sample_vMF

# データ選択
dataset = data.iloc[:,8:14]
# Spherical K-Means clustering

skm = SphericalKMeans(n_clusters=4, init='k-means++', n_init=1000)
skm.fit(dataset)

skm.cluster_centers_
skm.labels_
Counter(skm.labels_)

# ユークリッド距離
print("Silhouette Coefficient (euclidean): %0.3f"
      % metrics.silhouette_score(dataset, skm.labels_, metric='euclidean'))
print("Silhouette Coefficient (cosine): %0.3f"
      % metrics.silhouette_score(dataset, skm.labels_, metric='cosine'))

# データ書き出し
data["cluster_id"] = skm.labels_
data.to_csv('C:/Users/SHIO-160412-4/Desktop/data-competition/rmd/csv/customer_cluster.csv', index=False )

# Mixture of von Mises Fisher clustering (hard)
import scipy.sparse as sp
dummy = []
n_samples = dataset.shape[0]
dataset_ = np.array(dataset)
for ee in range(n_samples):
    if sp.issparse(dataset_):
        n = sp.linalg.norm(dataset_[ee, :])
    else:
        n = np.linalg.norm(dataset_[ee, :])

    if np.abs(n - 1.) > 1e-4:
        dummy.append([ee, n])

dataset_ = np.delete(dataset_, np.array(dummy)[:, 0], 0)

vmf_hard = VonMisesFisherMixture(n_clusters=4, posterior_type='soft', n_init=20)
vmf_hard.fit(dataset_)
