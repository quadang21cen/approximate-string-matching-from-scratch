"""
File: preprocessing.py
Author: Quach Dang
Description: Pre-processing data to prepare for searching
Date: December 07, 2023
"""

import sys
import io
sys.path.append('..\\approximate-string-matching\\data')
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

import pandas as pd
from unidecode import unidecode

path = "data\\Cities.xls"

def city2dict(path):
  pass
  df = pd.read_excel(path)
  # grouby
  city_df = df.groupby('Tỉnh Thành Phố')['Mã TP'].first().reset_index()
  dist_df = df.groupby('Quận Huyện')[['Mã TP','Mã QH']].first().reset_index()
  ward_df = df.groupby('Phường Xã')[['Mã QH','Mã PX']].first().reset_index()

  # processing
  # city_df['Tỉnh Thành Phố'] = city_df['Tỉnh Thành Phố'].apply(lambda row: unidecode(row.replace('Thành phố ','').replace('Tỉnh ','')).lower())  # remove marks
  city_df['Tỉnh Thành Phố'] = city_df['Tỉnh Thành Phố'].apply(lambda row: row.replace('Thành phố ','').replace('Tỉnh ','').lower())
  dist_df['Quận Huyện'] = dist_df['Quận Huyện'].apply(lambda row: row.replace('Quận ','').replace('Huyện ','').lower())
  ward_df['Phường Xã'] = ward_df['Phường Xã'].apply(lambda row: row.replace('Phường ','').replace('Xã ','').replace('Thị trấn ','').lower())

  #sorting
  # city_df = city_df.sort_values(by='Mã TP', ascending=True)
  # dist_df = dist_df.sort_values(by='Mã TP', ascending=True)
  # ward_df = ward_df.sort_values(by='Mã QH', ascending=True)

  # to dict
  dict_city = {row[1][1]:row[1][0] for row in city_df.iterrows()}
  dict_dist = {}
  for row in dist_df.iterrows():
    if row[1][1] not in dict_dist:
      dict_dist[row[1][1]] = {row[1][2]:row[1][0]}
    else:
      dict_dist[row[1][1]][row[1][2]] = row[1][0]

  dict_ward = {}
  for row in ward_df.iterrows():
    if row[1][1] not in dict_ward:
      dict_ward[row[1][1]] = {row[1][2]:row[1][0]}
    else:
      dict_ward[row[1][1]][row[1][2]] = row[1][0]

  given_data = {"city": dict_city,
                'dist': dict_dist,
                'ward': dict_ward}
  return given_data


if __name__ == "__main__":
  city2dict(path= path)