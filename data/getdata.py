"""
File: preprocessing.py
Author: Quach Dang
Description: Pre-processing data to prepare for searching
Date: December 07, 2023
"""

import sys
import io
sys.path.append('..\\approximate-string-matching')
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

import pandas as pd
from unidecode import unidecode

default_path = "data\\Cities.xls"

def city2dict(path = default_path):

  df = pd.read_excel(path)

  df = df.apply(lambda x: x.astype(str).str.lower())
  # grouby
  city_df = df.groupby('Tỉnh Thành Phố')['Mã TP'].first().reset_index()
  dist_df = df.groupby('Quận Huyện')['Tỉnh Thành Phố'].first().reset_index()
  ward_df = df.groupby('Phường Xã')['Quận Huyện'].first().reset_index()
  # processing
  # city_df['Tỉnh Thành Phố'] = city_df['Tỉnh Thành Phố'].apply(lambda row: unidecode(row.replace('Thành phố ','').replace('Tỉnh ','')).lower())  # remove marks
  city_df['Tỉnh Thành Phố'] = city_df['Tỉnh Thành Phố'].apply(lambda row: row.replace('thành phố ','').replace('tỉnh ',''))

  dist_df['Quận Huyện'] = dist_df['Quận Huyện'].apply(lambda row: row.replace('quận ','').replace('huyện ','').replace('thành phố ',''))
  dist_df['Tỉnh Thành Phố'] = dist_df['Tỉnh Thành Phố'].apply(lambda row: row.replace('thành phố ','').replace('tỉnh ',''))


  ward_df['Phường Xã'] = ward_df['Phường Xã'].apply(lambda row: row.replace('phường ','').replace('xã ','').replace('thị trấn ',''))
  ward_df['Quận Huyện'] = ward_df['Quận Huyện'].apply(lambda row: row.replace('quận ','').replace('huyện ',''))
  # to dict
  dict_city = [row[1][0] for row in city_df.iterrows()]
  dict_dist = {}

  for row in dist_df.iterrows():
    if row[1][1] not in dict_dist:
      dict_dist[row[1][1]] = [row[1][0]]
    else:
      dict_dist[row[1][1]].append(row[1][0])

  dict_ward = {}
  for row in ward_df.iterrows():
    if row[1][1] not in dict_ward:
      dict_ward[row[1][1]] = [row[1][0]]
    else:
      dict_ward[row[1][1]].append(row[1][0])
      
  return {"city": dict_city,
                'dist': dict_dist,
                'ward': dict_ward}

def full_address2list(path = default_path):
  list_address = []
  df = pd.read_excel(path)
  for row in df.iterrows():
    res = str(row[1][4]) +", " + str(row[1][2]) +", " + str(row[1][0])
    res = res.replace('Thành phố ','').replace('Tỉnh ','').replace('Quận ','').replace('Huyện ','').replace('Phường ','').replace('Xã ','').replace('Thị trấn ','').lower()
    list_address.append(res)
  return list_address

if __name__ == "__main__":
  data = city2dict(path = default_path)
  print(data)