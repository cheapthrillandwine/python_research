import time

start = time.perf_counter()
end = time.perf_counter()
# 累乗の計算(通常)
# n会の乗算が必要になる
def pow(x, n):
    x,n = 2, 10000
    start = time.perf_counter()
    value = 1
    while n > 0:
        value *= x
        n -= 1
    return value
    end = time.perf_counter()
    print(end-start)
# 累乗の計算(再帰定義)

def pow1(x, n):
    if n == 0:
        return 1
    value = pow1(x, n / 2)
    value += value
    if n % 2 == 1:
        value *= x
    return value
    print(pow1)

# 累乗の計算(繰り返し)
def pow2(x, n):
    value = 1
    while n > 0:
        if n & 1:
            value *= x
            n >>= 1
            x *= x
    return value
    print(pow2)
