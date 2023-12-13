"""
File: preprocessing.py
Author: Quach Dang
Description: Pre-processing data to prepare for searching
Date: December 07, 2023
"""

import sys
import io
sys.path.append('..\\approximate-string-matching-from-scratch\\data')
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

import getdata
import distance

class Fuzzy_Search_Address:
    def __init__(self, data) -> None:
        self.dict_city = data['city']
        self.dict_dist = data['dist']
        self.dict_ward = data['ward']
        

    def search_address(self, query):
        query = query.lower()
        city_query = None
        dist_query = None
        ward_query = None
        if "," in query:
            arr_query  = query.split(',')
            city_query = arr_query[-1].lstrip()
            dist_query = arr_query[-2].lstrip()
            ward_query = arr_query[-3].lstrip()
        else:
            arr_query  = query.split(' ')
            city_query =  arr_query[-3:].lstrip()
            dist_query =  arr_query[-6:-3].lstrip()
            ward_query =  arr_query[-9:-3].lstrip()
      
        
        city_result = fuzzy_search(query=city_query,data= self.dict_city)[0][0]
        dist_result = fuzzy_search(query=dist_query,data= self.dict_dist[city_result])[0][0]
        ward_result = fuzzy_search(query=ward_query,data= self.dict_ward[dist_result])[0][0]
        
        return {    "result": {
                            "province": city_result,
                            "district": dist_result,
                            "ward": ward_result
                            }}

def fuzzy_search(query, data, threshold=0.2):
    if query in data:
        return [(query,0.5)]
    results = []
    for item in data:
        similarity = distance.calculate_similarity(query, item)
        if similarity >= threshold:
            results.append((item, similarity))
    results.sort(key=lambda x: x[1], reverse=True)
    return results





if __name__ == "__main__":
    import time
    DATA = getdata.city2dict()
    address_search = Fuzzy_Search_Address(DATA)
    start_time = time.time()
    result = address_search.search_address(query="Đá Hàng Hiệp Thạnh, Gò Dầu, Tây Ninh")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Thời gian thực thi': {execution_time:.6f} giây")
    print(result)



\
