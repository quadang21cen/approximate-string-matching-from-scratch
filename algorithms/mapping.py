import distance
input_s = "ooannw"
data_set = ["applee", "bbnana", "ooange", "graaea", "wateem", "kiiiho"]
sim_list = []


import numpy as np

def calculate_cosine_similarity(vector1, vector2):
    norm_vector1 = np.linalg.norm(vector1)
    norm_vector2 = np.linalg.norm(vector2)
    
    if norm_vector1 == 0 or norm_vector2 == 0:
        return 0  # Tránh chia cho 0
    
    cosine_sim = np.dot(vector1, vector2) / (norm_vector1 * norm_vector2)
    return cosine_sim


def string_to_ascii_vector(input_string):
    ascii_vector = [ord(char) for char in input_string]
    return ascii_vector

ascii_list = [string_to_ascii_vector(value) for value in data_set]
mapping_ascii = string_to_ascii_vector("qwerxa")


for row in ascii_list:
    sim_list.append(calculate_cosine_similarity(mapping_ascii,row))


input_ascii = string_to_ascii_vector(input_s)
sim_input_mapping = calculate_cosine_similarity(input_ascii,mapping_ascii)
result_vec = []

for row in sim_list:
    result_vec.append(abs(sim_input_mapping - row))

print(result_vec)

print(min(result_vec))