#python 3 program to demonstrate working of BK-Tree
import queue
 
class Node:
    def __init__(self, x=None):
        self.word = x
        self.next = [0] * 20
 
def add(root, curr):
    if not root.word:
        root.word = curr.word
        root.next = curr.next
        return
 
    dist = edit_distance(curr.word, root.word)
    if not tree[root.next[dist]] or not tree[root.next[dist]].word:
        global ptr
        ptr += 1
        tree[ptr] = curr
        root.next[dist] = ptr
    else:
        add(tree[root.next[dist]], curr)
 
def get_similar_words(root, s):
    ret = []
    if not root or not root.word:
        return ret
 
    dist = edit_distance(root.word, s)
    if dist <= TOL:
        ret.append(root.word)
 
    start = dist - TOL if dist - TOL > 0 else 1
    while start <= dist + TOL:
        tmp = get_similar_words(tree[root.next[start]], s)
        ret += tmp
        start += 1
    return ret
 
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
                dp[i][j] = min(
                    dp[i - 1][j] + 1,  # deletion
                    dp[i][j - 1] + 1,  # insertion
                    dp[i - 1][j - 1] + 1  # replacement
                )
            else:
                dp[i][j] = dp[i - 1][j - 1]
    return dp[m][n]
 
MAXN = 100
TOL = 2
LEN = 10
 
RT = Node()
tree = [Node() for _ in range(MAXN)]
ptr = 0
#dictionary words
if __name__ == "__main__":
    dictionary = ["hell", "help", "shell", "smell", "fell", "felt", "oops", "pop", "oouch", "halt"]
    sz = len(dictionary)
    #adding dict[] words on to tree
    for i in range(sz):
        tmp = Node(dictionary[i])
        add(RT, tmp)
 
    w1 = "ops"
    match1 = get_similar_words(RT, w1)
    print("similar words in dictionary for", w1, ": ")
    for word in match1:
        print(word, end=" ")
    print()
 
    #this code is contributed by NarasingaNikhil