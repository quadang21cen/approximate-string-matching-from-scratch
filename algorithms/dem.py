def miniMaxSum(arr):
    # arr = sorted(arr)
    print(arr)
    min_res = arr[2:3]
    max_res = arr[1:3]
    return min_res, max_res
    
if __name__ == '__main__':
    arr = "1 2 3 4 5"
    arr = list(map(int, input().rstrip().split()))
    print(miniMaxSum(arr))