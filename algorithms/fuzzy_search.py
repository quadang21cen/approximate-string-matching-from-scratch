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


def fuzzy_search(query, data, threshold=0.7):
    """
    Hàm thực hiện fuzzy search đơn giản từ đầu.

    Parameters:
    - query: Chuỗi cần tìm kiếm.
    - data: Danh sách các chuỗi trong tập dữ liệu.
    - threshold: Ngưỡng tương đồng để xem xét một kết quả là tìm thấy hay không.
    Returns:
    - Kết quả tìm kiếm gần giống với query.
    """
    results = []

    for item in data:
        similarity = calculate_similarity(query, item)
        if similarity >= threshold:
            results.append((item, similarity))

    # Sắp xếp theo độ tương đồng giảm dần
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


def levenshtein_distance(str1, str2):
    len_str1 = len(str1)
    len_str2 = len(str2)

    # Tạo ma trận Levenshtein với một dòng và một cột phụ
    matrix = [[0] * (len_str2 + 1) for _ in range(len_str1 + 1)]

    # Khởi tạo giá trị đầu tiên của ma trận
    for i in range(len_str1 + 1):
        matrix[i][0] = i
    for j in range(len_str2 + 1):
        matrix[0][j] = j

    # Điền ma trận dựa trên giá trị của các hàng và cột trước đó
    for i in range(1, len_str1 + 1):
        for j in range(1, len_str2 + 1):
            cost = 0 if str1[i - 1] == str2[j - 1] else 1
            matrix[i][j] = min(
                matrix[i - 1][j] + 1,      # Xóa
                # matrix[i][j - 1] + 1,      # Chèn
                # matrix[i - 1][j - 1] + cost  # Thay thế
            )

    return matrix[len_str1][len_str2]

# Hàm này trả về độ tương đồng, vì vậy càng nhỏ là càng giống
def calculate_levenshtein_similarity(str1, str2):
    max_len = max(len(str1), len(str2))
    distance = levenshtein_distance(str1, str2)
    similarity = 1 - distance / max_len
    return similarity


if __name__ == "__main__":
    # Ví dụ sử dụng
    data_set = ["apple", "banana", "orange", "grape", "watermelon", "kiwi"]
    query_string = "appl"
    search_results = fuzzy_search(query_string, data_set)
    print("Kết quả tìm kiếm gần giống với '{}':".format(query_string))
    for result, similarity in search_results:
        print(" - {}: {:.2f}".format(result, similarity))
