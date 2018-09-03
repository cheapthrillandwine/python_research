# 二重再帰
# 同じ値を何回も求めているため、効率が悪い
def fico(n):
    if n == 0 or n == 1:
        return 1
    return fibo(n-1) + fibo(n-2)

# 末尾再帰
# 累積変数a1,a2を使って、現在のフィボナッチ数をa1にひとつ前伊の値をa2に格納する
def fibo(n, a1 = 1, a2 = 0):
    if n < 1:
        return a1
    return fibo(n - 1, a1 + a2, a1)

# 繰り返し
def fibo(n):
    a1, a2 = 1, 0
    while n > 0:
        a1, a2 = a1 + a2, a1
        n -= 1
    return a1
