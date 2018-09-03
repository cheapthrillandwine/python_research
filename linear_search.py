# pure python
# 計算量O(n)
# ソートは関係ない=先頭から探索していくため
# a = [1,2,3,4,5,6,7,8,9,10]
# x = 5
# for i in range(0, len(a)):
#     if x == a[i]:
#         print(f"{x} is exist")
#         break
#     elif x == (len(a) - 1):
#         print(f"{x} is not found")

from random import shuffle

def linear_search(a, value):
    for x in a:
        if x == value:
            print(f"{value} is exist")
            return True
            break
        else:
            print(f"{value} is not found")
            return False

if __name__ == '__main__':
    a = range(15)
    for num in a:
        assert linear_search(a, num)
    assert linear_search(a, 15) == False
    assert linear_search(a, 14) == True
    assert linear_search(a, 0) == True
    assert linear_search(a, 2) == True
    assert linear_search(a, 4) == True
    assert linear_search(a, 5) == True
    assert linear_search(a, 6) == True


    # v = input('Find value? ')
    # r = linear_search(a, int(v))
    # if r:
    #     print('Found!')
    # else:
    #     print('Not Found!')
