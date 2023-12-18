"""
File: preprocessing.py
Author: Quach Dang
Editor: Thai Tran
Date: December 15, 2023
Description: Pre-processing data to prepare for searching
"""

import sys
import io
import pandas as pd
import json


def preprocessing(text):
    text = text.lower()
    replacements = ["tp.","tp","tt",".", "xã","thành","huyện",",,", "tỉnh"]
    for replacement in replacements:
        text = text.replace(replacement, "")
    return text.strip()
###INPUT###
def test_data(path = "/content/drive/MyDrive/Address_Classification_Group_2_IMP_15122023/Fuzzy_search/public_new.json"):
  with open(path, 'r', encoding='utf-8-sig') as file:
        data = json.load(file)
  return data

default_path = "/content/drive/MyDrive/Address_Classification_Group_2_IMP_15122023/Fuzzy_search/Cities.xls"
###INPUT###
def city2dict(path = default_path):

  df = pd.read_excel(path)

  df = df.apply(lambda x: x.astype(str).str.lower())
  # grouby
  city_df = df.groupby('Tỉnh Thành Phố')['Mã TP'].first().reset_index()
  dist_df = df.groupby('Quận Huyện')['Tỉnh Thành Phố'].first().reset_index()
  ward_df = df.groupby('Phường Xã')['Quận Huyện'].first().reset_index()
  # processing
  # city_df['Tỉnh Thành Phố'] = city_df['Tỉnh Thành Phố'].apply(lambda row: unidecode(row.replace('Thành phố ','').replace('Tỉnh ','')).lower())  # remove marks
  city_df['Tỉnh Thành Phố'] = city_df['Tỉnh Thành Phố'].apply(lambda row: row.replace('thành phố ','').replace('tỉnh ','').replace('huyện ','').replace(" - "," "))

  dist_df['Quận Huyện'] = dist_df['Quận Huyện'].apply(lambda row: row.replace('quận ','').replace('huyện ','').replace('thành phố ','').replace("thị xã ",""))
  dist_df['Tỉnh Thành Phố'] = dist_df['Tỉnh Thành Phố'].apply(lambda row: row.replace('thành phố ','').replace('tỉnh ','').replace('huyện ','').replace(" - "," "))

  ward_df['Phường Xã'] = ward_df['Phường Xã'].apply(lambda row: row.replace('phường ','').replace("thị xã ","").replace('xã ','').replace('thị trấn ','').replace("thành phố ",""))
  ward_df['Quận Huyện'] = ward_df['Quận Huyện'].apply(lambda row: row.replace('quận ','').replace('huyện ','').replace("thị xã ","").replace("thành phố ","").replace("xã ",""))

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

class Fuzzy_Search_Address:
    def __init__(self, data) -> None:
        self.dict_city = data['city']
        self.dict_dist = data['dist']
        self.dict_ward = data['ward']


    def search_address(self, query):

        query = preprocessing(query)
        city_query = None
        dist_query = None
        ward_query = None

        city_result = None
        dist_result = None
        ward_result = None
        # simple querry
        if "," in query and len(query.split(',')) >= 3:

            arr_query  = query.split(',')
            city_query = arr_query[-1]
            dist_query = arr_query[-2]
            ward_query = arr_query[-3]

            try:
                city_result = fuzzy_search(query=city_query,data= self.dict_city)[0][0]
                dist_result = fuzzy_search(query=dist_query,data= self.dict_dist[city_result])[0][0]
                ward_result = fuzzy_search(query=ward_query,data= self.dict_ward[dist_result])[0][0]
            except:
                pass

        # # complex querry
        else:
            arr_query  = query.split(' ')
            sta_num = -2
            end_num = 0
            # search city
            while city_result == None:
                city_query =  " ".join(arr_query[sta_num:])
                fuz_result = fuzzy_search(query=city_query,data= self.dict_city)
                if fuz_result != []:
                    temp = sta_num
                    sta_num = sta_num -2
                    end_num = temp
                    city_result = fuz_result[0][0]
                    break
                if fuz_result == []:
                    sta_num = sta_num - 1
                else:
                    temp = sta_num
                    sta_num = sta_num -2
                    end_num = temp
                    city_result = fuz_result[0][0]
                    break


            while dist_result == None:
                dist_query =  " ".join(arr_query[sta_num:end_num])
                try:
                    fuz_result = fuzzy_search(query=dist_query,data= self.dict_dist[city_result])
                except:
                    return {"result": {
                            "province": city_result,
                            "district": dist_result,
                            "ward": ward_result
                            }}
                if fuz_result != []:
                    temp = sta_num
                    sta_num = sta_num -2
                    end_num = temp
                    dist_result = fuz_result[0][0]
                elif abs(sta_num - end_num) > 3:
                    return {"result": {
                            "province": city_result,
                            "district": dist_result,
                            "ward": ward_result
                            }}
                elif fuz_result == []:
                    sta_num = sta_num - 1

            while ward_query == None:
                ward_query =  " ".join(arr_query[sta_num:end_num])
                try:
                    fuz_result = fuzzy_search(query=ward_query,data = self.dict_ward[dist_result])
                except:
                    break
                if fuz_result != []:
                    temp = sta_num
                    sta_num = sta_num -2
                    end_num = temp
                    ward_query = fuz_result[0][0]
                elif abs(sta_num - end_num) > 3:
                    temp = sta_num
                    sta_num = sta_num -2
                    end_num = temp
                    return {"result": {
                            "province": city_result,
                            "district": dist_result,
                            "ward": ward_result
                            }}
                elif fuz_result == []:
                    sta_num = sta_num - 1
        # search city
        if city_result is None:
          city_result = ""
        else:
          city_result = ' '.join(word.capitalize() for word in city_result.split())
        if dist_result is None:
          dist_result = ""
        else:
          dist_result = ' '.join(word.capitalize() for word in dist_result.split())
        if ward_result is None:
          ward_result = ""
        else:
          ward_result = ' '.join(word.capitalize() for word in ward_result.split())
        address_dict = {}
        address_dict["result"] = {"province":city_result, "district":dist_result, "ward":ward_result}
        return address_dict

def fuzzy_search(query, data, threshold=0.2):
    query = query.strip().replace(",","")
    if query in data:
        return [(query,0.9)]
    results = []
    for item in data:
        similarity = calculate_similarity(query, item)
        if similarity >= threshold:
            results.append((item, similarity))
    results.sort(key=lambda x: x[1], reverse=True)
    return results

def calculate_similarity(str1, str2):
    len_str1 = len(str1)
    len_str2 = len(str2)
    max_len = max(len_str1, len_str2)

    #  Jaccard
    intersection = len(set(str1) & set(str2))
    union = len(set(str1) | set(str2))
    jaccard_similarity = intersection / union if union != 0 else 0

    # Cosine
    dot_product = sum(ord(a) * ord(b) for a, b in zip(str1, str2))

    norm_str1 = sum(ord(a) ** 2 for a in str1) ** 0.5
    norm_str2 = sum(ord(b) ** 2 for b in str2) ** 0.5
    cosine_similarity = dot_product / (norm_str1 * norm_str2) if norm_str1 * norm_str2 != 0 else 0

    # Lấy trung bình cộng của độ tương đồng Jaccard và Cosine
    average_similarity = (jaccard_similarity + cosine_similarity) / 2

    return average_similarity

if __name__ == "__main__":
    import time
    import json
    DATA = city2dict()
    address_searcher = Fuzzy_Search_Address(data = DATA)
    TEST_DATA = test_data()
    arr_result = {}
    timer = []
    list_cover_score = []
    for data in TEST_DATA:
        #Start time
        start = time.perf_counter_ns()
        res = address_searcher.search_address(query=data['text'])
        test_data()
        arr_result.update({"text":data["text"], "result": res["result"]})
        #Stop time
        finish = time.perf_counter_ns()
        running_time_s = (finish - start) / 1e9
        timer.append(running_time_s)
        count_cover = 0
        for i in range(0,len(list(data["result"]))):
          count = 0
          for j in range(0,len(list(arr_result["result"]))):
            if data["result"][list(data["result"])[i]] == arr_result["result"][list(arr_result["result"])[j]]:
              count = 1
          count_cover += count
        list_cover_score.append(count_cover)

    # ###OUTPUT###
    # json_file_path = '/content/drive/MyDrive/Address_Classification_Group_2_IMP_15122023/Fuzzy_search/output_samples/public_new_fixed_Fuzzy.json'
    # ###OUTPUT###
    
    correct = 0
    for count in list_cover_score:
        if count == 3:
            correct += 1
    total = len(list_cover_score)
    print(f"correct = {correct}/{total} ({correct / total * 10:.2f} / 10)")

    max_timer = max(timer)
    mean_timer = sum(timer) / len(timer)
    
    print(f"max_time = {max_timer:.4f} seconds")
    print(f"mean_time = {mean_timer:.4f} seconds")
    with open(json_file_path, 'w', encoding='utf-8-sig') as json_file:
        json.dump(arr_result, json_file, ensure_ascii=False, indent=2)

    print(f'Dictionary đã được lưu vào file: {json_file_path}')
