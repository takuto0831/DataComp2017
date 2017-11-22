# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 17:41:41 2017

@author: SHIO-160412-4
"""
import requests
import json
import pandas as pd

a = pd.read_csv("rmd/csv/zeocode.csv")
url = 'http://geoapi.heartrails.com/api/json'

a = a.drop(i)
a = a.reset_index(drop=True)

for i in range(len(a)):
#for i in range(5):
    payload = {'method':'searchByPostal'}
    payload['postal']= str(a.iloc[i,0])
    res = requests.get(url, params=payload).json()['response']['location'][0]
    series = pd.Series([res['y'],res['x']], index=data.columns)
    data = data.append(series, ignore_index = True)

while True:
    data = pd.DataFrame(index=[], columns=['column1', 'column2'])
    try:
        for i in range(len(a)):
            payload = {'method':'searchByPostal'}
            payload['postal']= str(a.iloc[i,0])
            res = requests.get(url, params=payload).json()['response']['location'][0]
            series = pd.Series([res['y'],res['x']], index=data.columns)
            data = data.append(series, ignore_index = True)
        break
    except:
        a = a.drop(i)
        a = a.reset_index(drop=True)
        
    
response = pd.concat([a, data], axis=1)
response.to_csv('rmd/csv/zeocode_plus.csv',index=False )
