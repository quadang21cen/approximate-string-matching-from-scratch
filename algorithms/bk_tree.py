#python 3 program to demonstrate working of BK-Tree
import queue
import sys
import io
sys.path.append('..\\approximate-string-matching')
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

class Node:
    def __init__(self, x=None):
        self.word = x
        self.next = [0] * 20

class BKTree:
    def __init__(self):
        self.root = Node()
        self.tree = [Node() for _ in range(100)]
        self.ptr = 0

    def add(self, root, curr):
        if not root.word:
            root.word = curr.word
            root.next = curr.next
            return
        dist = self.edit_distance(curr.word, root.word)
        if not self.tree[root.next[dist]] or not self.tree[root.next[dist]].word:
            self.ptr += 1
            self.tree[self.ptr] = curr
            root.next[dist] = self.ptr
        else:
            self.add(self.tree[root.next[dist]], curr)

    def get_similar_words(self, root, s):
        ret = []
        if not root or not root.word:
            return ret

        dist = self.edit_distance(root.word, s)
        if dist <= TOL:
            ret.append(root.word)

        start = dist - TOL if dist - TOL > 0 else 1
        while start <= dist + TOL:
            tmp = self.get_similar_words(self.tree[root.next[start]], s)
            ret += tmp
            start += 1
        return ret

    @staticmethod
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

class bk_tree_search:

    def __init__(self, dict_data):
        self.dict_city = dict_data['city']
        self.dict_dist = dict_data['dist']
        self.dict_ward = dict_data['ward']

        bktree_city = BKTree()
        for word in self.dict_city:
            tmp = Node(word)
            bktree_city.add(bktree.root, tmp)

        for word in self.dict_data['dist']

        print(self.dict_dist)

    def search(self,input):
        pass



if __name__ == "__main__":
    TOL = 3
    bktree = BKTree()
    
    # # # Dictionary words
    # dictionary = ["hell", "help", "shell", "smell", "fell", "felt", "oops", "pop", "oouch", "halt"]
    # for word in dictionary:
    #     tmp = Node(word)
    #     bktree.add(bktree.root, tmp)
    # w1 = "help"
    # match1 = bktree.get_similar_words(bktree.root, w1)
    # print(match1)


    from data import getdata as gd
    DATA = gd.address2list()
    # dict_city = DATA["city"]
    # dict_city_name_id = {dict_city[key]: key for key in dict_city}

    # list_city = [dict_city[key] for key in dict_city]

    for word in DATA[:20]:
        tmp = Node(word)
        bktree.add(bktree.root, tmp)
    w1 = "TT Tân Bình Huyện Yên Sơn, Tuyên Quang"
    match1 = bktree.get_similar_words(bktree.root, w1)
    # id_match = dict_city_name_id[match1[0]]
    print(match1)

    # dict_dist = DATA["dist"]
    # print(dict_dist[id_match])


    # search = bk_tree_search(dict_data = DATA)



 