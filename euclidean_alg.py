# p = 54
# q = 39
def GCD(p,q):
    while True:
        r = p % q
        if r == 0:
            return q
        p, q = q, r
        print(r)
