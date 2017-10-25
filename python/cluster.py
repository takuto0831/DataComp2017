# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 16:33:31 2017

@author: SHIO-160412-4
"""
import codecs
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from collections import Counter

# ファイル読み込み
with codecs.open("C:/Users/SHIO-160412-4/Desktop/data-competition/rmd/csv/customer.csv", "r", "Shift-JIS", "ignore") as file:
    data = pd.read_table(file, delimiter=",")
# フリー女性, フリー男性, 顧客情報なしのデータを消去する.
data = data.drop([989,5384,6137,11031,990,6136])

# クラスタリング
# 時間別来店数のデータを numpy 形式に変更
cust_array = np.array([data['morning_count_weekday'].tolist(),
                       data['evening_count_weekday'].tolist(),
                       data['night_count_weekday'].tolist(),
                       data['morning_count_holiday'].tolist(),
                       data['evening_count_holiday'].tolist(),
                       data['night_count_holiday'].tolist()], np.int32)
# 配列を転置
cust_array = cust_array.T

# クラスタリング
# もっと細かい変数を指定できる？
# クラスタリングに項目の平均を使いたくない、６方向のベクトルをそれぞれ独立に使いたいイメージ

pred1 = KMeans(n_clusters=4,max).fit_predict(cust_array)

# クラスタリングの結果を元データに結合
data["cluster_id"] = pred

# クラスとリングした結果を用いてヒストグラム
plt.hist(data[data["cluster_id"] == 0]["total_item_money"], bins=50)
plt.hist(data[data["cluster_id"] == 1]["total_item_money"], bins=50)
plt.hist(data[data["cluster_id"] == 2]["total_item_money"], bins=50)
plt.hist(data[data["cluster_id"] == 3]["total_item_money"], bins=50)
#plt.hist(data[data["cluster_id"] == 4]["total_item_money"], bins=50)
#plt.hist(data[data["cluster_id"] == 5]["total_item_money"], bins=50)

# 同じく来店間隔の平均
### 結構ちがくておもしろいかも！！！！！！！！！！！
data[data["cluster_id"] == 0]["visit_interval"].mean()
data[data["cluster_id"] == 1]["visit_interval"].mean()
data[data["cluster_id"] == 2]["visit_interval"].mean()
data[data["cluster_id"] == 3]["visit_interval"].mean()
#data[data["cluster_id"] == 4]["visit_interval"].mean()
#data[data["cluster_id"] == 5]["visit_interval"].mean()

# データ書き出し
data.to_csv('C:/Users/SHIO-160412-4/Desktop/data-competition/rmd/csv/customer_cluster.csv', index=False )
