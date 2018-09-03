# binary_search
# 計算量O(logN)
# using library
# listの昇順を苦座さずに挿入できる位置を返す
# リスト要素がすべてわかっていないと使えない
# ソートされている必要がある
# import bisect
#
# a = [1,2,3,4,5,6,7,8,9,10]
# x = 5
# ins_i = bisect.bisect_left(a,x)
# a.insert(ins_i,x)
#
# print(a)


# pure python
# a = [1,2,3,4,5,6,7,8,9,10]
# low = 0
# high = len(a) - 1
# x = 5
#
# while low <= high:
#     binary = (low + high) // 2
#     predict = a[binary]
#     if predict == x:
#         print(f"{x} is exist.")
#         return True
#         break
#     elif predict < x:
#         low = binary + 1
#     else:
#         high =  - 1
# if predict != x:
#     print(f"{x} is not found.")
#     return False

import sys

def binary_search(a, value):
    low = 0
    high = len(a) - 1

    while low <= high:
        binary = (low + high) // 2
        predict = a[binary]
        if predict == value:
            print(f"{value} is exist.")
            return True
            break
        elif predict < value:
            low = binary + 1
        else:
            high = binary - 1
    print(f"{value} is not found.")
    return False

if __name__ == '__main__':
    a = range(15)
    for num in a:
        assert binary_search(a, num)
    assert binary_search(a, -30) == False
    assert binary_search(a, 15) == False
    assert binary_search(a, 14) == True
    assert binary_search(a, 0) == True
    assert binary_search([1,2,3,4,5,6,20], 3) == False
