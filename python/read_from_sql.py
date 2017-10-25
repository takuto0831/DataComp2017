# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 16:48:34 2017

@author: SHIO-160412-4
"""
import codecs
import os
import psycopg2
import pandas as pd

# データベース接続
cnn = psycopg2.connect("dbname=datacom2017 host=192.168.11.16 user=postgres port=5432 password=postgres")
scan= "C:/Users/SHIO-160412-4/Desktop/data-competition/sql/tmp.sql"

query = codecs.open(scan, 'r', 'utf-8').read()
with cnn.cursor() as cursor:
    cursor.execute(query)
    data = pd.DataFrame(cursor.fetchall())

# 列名がさくじょされるので追加
name = ["customer_id","first_year","first_store","zip_code","dm","sex","birth_age","comment",
        "morning_count_weekday","evening_count_weekday","night_count_weekday","morning_count_holiday",
        "evening_count_holiday","night_count_holiday","remake_count","total_item_money","visit_interval"]
data.columns = name
