import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer
from collections import Counter

# データ読み込み関数
store_csv = pd.read_csv("csv/StoreMaster.csv",encoding="SHIFT-JIS") 
staff_csv = pd.read_csv("csv/StaffMaster.csv",encoding="SHIFT-JIS") 
customer_csv = pd.read_csv("csv/CustomerMaster.csv",encoding="SHIFT-JIS")
 
item_csv = pd.read_csv("csv/ItemMaster.csv", encoding="SHIFT-JISX0213") 
AccountAbout_csv = pd.read_csv("csv/AccountAbout.csv",encoding="SHIFT-JIS") 
AccountHistory_csv = pd.read_csv("csv/AccountHistory.csv",encoding="SHIFT-JIS") 

# データ基本確認事項
store_csv.dtypes
staff_csv.dtypes
customer_csv.dtypes
item_csv.dtypes
AccountAbout_csv.dtypes
AccountHistory_csv.dtypes

# 特徴量ごとにデータ欠損が含まれているか調べる
store_csv.isnull().any(axis=0)
staff_csv.isnull().any(axis=0)
customer_csv.isnull().any(axis=0)
item_csv.isnull().any(axis=0)
AccountAbout_csv.isnull().any(axis=0)
AccountHistory_csv.isnull().any(axis=0)

# 欠損値の個数をカウント
customer_csv.isnull().sum()
item_csv.isnull().sum()
AccountAbout_csv.isnull().sum()
AccountHistory_csv.isnull().sum()

#基本統計量
store_csv.describe()
staff_csv.describe()
customer_csv.describe()
item_csv.describe()
AccountAbout_csv.describe()
AccountHistory_csv.describe()

# 各特長量の種類をカウントする関数
def LevelCount(data):
    n = data.shape[1]
    for i in range(n):
        print(len(Counter(data.iloc[:,i])))

LevelCount(store_csv)
LevelCount(staff_csv)
LevelCount(customer_csv)
LevelCount(item_csv)
LevelCount(AccountAbout_csv)
LevelCount(AccountHistory_csv)


# 返品処理 
# 全てをまとめたデータを作成する
tmp = pd.merge(AccountHistory_csv,AccountAbout_csv,on = "会計ID")
All_data = pd.merge(tmp,item_csv,on = "会計明細販売商品ID",how = "left")

#　当日中に変更されたものはレジうち間違いと判断する
idx_list = ['会計ID', '販売店舗ID', '顧客ID', '会計税込売上', '会計消費税',
            "取引種別",'POS入力担当者ID', '会計主担当者ID','現金', 'クレジット','電子マネー']
idx_list2 = ['販売店舗ID', '顧客ID', '会計税込売上', '会計消費税',
            'POS入力担当者ID', '会計主担当者ID','現金', 'クレジット','電子マネー']
henpin_box = AccountHistory_csv.ix[:,idx_list]

# 金額関連のマイナスを調整
idx_money = ["会計税込売上","会計消費税","現金","クレジット","電子マネー"]
henpin_box.loc[:,idx_money] = abs(henpin_box.loc[:,idx_money])

List = []
for i in range(len(henpin_box)):
    if henpin_box.ix[i,"取引種別"] == "返品":
        j = 1
        while i-j >= 0:
            if all(henpin_box.ix[i-j,idx_list2] == henpin_box.ix[i,idx_list2]) and not henpin_box.ix[i-j,"会計ID"] in List:
                List.append(henpin_box.ix[i-j,"会計ID"])
                List.append(henpin_box.ix[i,"会計ID"])
                break
            j += 1
            
# 問題のある会計ID
BadList = pd.DataFrame({"会計ID":List})
# 問題のない会計ID 
GoodList = pd.DataFrame({"会計ID":list(set(henpin_box["会計ID"]) - set(List))})

AllBad = pd.merge(BadList,All_data,on = "会計ID", how = "left")
AllGood = pd.merge(All_data,GoodList,on = "会計ID")

# 返品は622件残る
Counter(AllGood["取引種別"])
