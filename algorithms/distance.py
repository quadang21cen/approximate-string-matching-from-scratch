def levenshtein_distance(str1, str2):
    len_str1 = len(str1)
    len_str2 = len(str2)
    # Create a Levenshtein matrix with one row and one extra column
    matrix = [[0] * (len_str2 + 1) for _ in range(len_str1 + 1)]
    print(matrix)
    # Initialize the first value of the matrix
    for i in range(len_str1 + 1):
        matrix[i][0] = i
    for j in range(len_str2 + 1):
        matrix[0][j] = j

    # Fill the matrix based on the values of previous rows and columns
    for i in range(1, len_str1 + 1):
        for j in range(1, len_str2 + 1):
            cost = 0 if str1[i - 1] == str2[j - 1] else 1
            # matrix[i][j] = matrix[i - 1][j] + 1
            matrix[i][j] = min(
                matrix[i - 1][j] + 1,           # delete
                matrix[i][j - 1] + 1,           # insert
                matrix[i - 1][j - 1] + cost     # replace
            )

    return matrix[len_str1][len_str2]

def compare_distance(text1, text2):
    text1 = [c for c in text1] 
    text2 = [c for c in text2]
    max_len = max(len(text1),len(text2))
    equal = 0
    for wor1 in text1:
        for wor2 in range(len(text2)):
            if wor1 == text2[wor2]:
                equal = equal + 1
                del text2[wor2]
                break
    diff = max_len - equal
    return diff


def edit_distance(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] != b[j - 1]:
                # dp[i][j] = dp[i - 1][j] + 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1,  # deletion
                    dp[i][j - 1] + 1,  # insertion
                    dp[i - 1][j - 1] + 1  # replacement
                )

            else:
                dp[i][j] = dp[i - 1][j - 1]
    # print(dp[m][n])
    return dp[m][n]

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
    sim = edit_distance("aacc","aacdceac4")
    print(sim)