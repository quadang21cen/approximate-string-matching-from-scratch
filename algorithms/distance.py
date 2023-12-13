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
                matrix[i][j - 1] + 1,      # Chèn
                matrix[i - 1][j - 1] + cost  # Thay thế
            )

    return matrix[len_str1][len_str2]

def compare_texts(text1, text2):
    text1 = [c for c in text1] 
    text2 = [c for c in text2]
    equal = 0
    for wor1 in text1:
        for wor2 in range(len(text2)):
            if wor1 == text2[wor2]:
                equal = equal + 1
                del text2[wor2]
                print(text2)
                break
    diff = len(text1) - equal
    return equal, diff


sim = levenshtein_distance("aa","aa")
print(sim)