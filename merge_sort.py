from random import shuffle

def merge_sort(a):
    if len(a) == 1:
        return

    num = len(a)
    a1 = [a.pop() for _ in range(num // 2)]
    a2 = [a.pop() for _ in range(num - num // 2)]
    merge_sort(a1)
    merge_sort(a2)

    a1.reverse()
    a2.reverse()
    while a1 and a2:
        if a1[-1] <= a2[-1]:
            a.append(a1.pop())
        else:
            a.append(a2.pop())

    while a1:
        a.append(a1.pop())

    while a2:
        a.append(a2.pop())

a = list(range(100))
shuffle(a)
merge_sort(a)
print(a)
print(len(a))
