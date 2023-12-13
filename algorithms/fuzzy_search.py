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
      
        
        city_result = fuzzy_search(query=city_query,data= self.dict_city)
        dist_result = fuzzy_search(query=dist_query,data= self.dict_dist[city_result])
        print(self.dict_ward[dist_result])
        ward_result = fuzzy_search(query=ward_query,data= self.dict_ward[dist_result])
        

        # print(city_result)
        # print(self.dict_dist[city_result])
        # print(dist_result)

def fuzzy_search(query, data, threshold=0.2):

    if query in data:
        return query
    results = []
    for item in data:
        similarity = distance.calculate_similarity(query, item)
        if similarity >= threshold:
            results.append((item, similarity))

    results.sort(key=lambda x: x[1], reverse=True)
    print("---------")
    
    print(query)
    print(results)
    print(data)
    return results[0][0]





if __name__ == "__main__":
    DATA = getdata.city2dict()
    address_search = Fuzzy_Search_Address(DATA)
    address_search.search_address(query="Nà Làng Phú Bình, Chiêm Hoá, Tuyên Quang")




    # # Ví dụ sử dụng
    # data_set = ["apple", "banana", "orange", "grape", "watermelon", "kiwi"]
    # query_string = "appl"
    # search_results = fuzzy_search(query_string, data_set)
    # print("Kết quả tìm kiếm gần giống với '{}':".format(query_string))
    # for result, similarity in search_results:
    #     print(" - {}: {:.2f}".format(result, similarity))
