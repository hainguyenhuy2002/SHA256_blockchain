def sigma(i,j,l):
    k = []
    for ia, ja, la in zip(i, j, l):
        a = ja ^ la
        b = ia ^ a
        k.append(b)
    return k


def add(i, j):
    length = len(i)
    sums = list(range(length))
    c = 0
    for x in range(length-1,-1,-1):
        sums[x] = sigmaa(i[x], j[x], c)
        c = maj(i[x], j[x], c)
    return sums


def ADD(x: list, y: list):
    assert len(x) == len(y)
    sum = []
    mem = 0
    for i in range(len(x) - 1, -1, -1):
        _x, _y = x[i], y[i]
        s = _x + _y + mem
        if s > 1:
            mem = 1
            s = s % 2
        else:
            mem = 0
        sum.append(s)
    return sum[::-1]


def NOT(x: list):
    k = []
    for i in x:
        k.append(1 - i)
    return k


def AND(x: list, y: list):
    k = []
    for ia, ja in zip(x, y):
        a = ia & ja
        k.append(a)
    return k


def XOR(x: list, y: list): 
    k = []
    for ia, ja in zip(x, y):
        a = ia ^ ja
        k.append(a)
    return k


def ROTR(x: list, n: int): 
    return x[-n:] + x[:-n]


def SHR(x: list, n: int): 
    return [0 for _ in range(n)] + x[:-n]


def SIGMA(x: list, r1, r2, s3):
    return XOR(XOR(ROTR(x, r1), ROTR(x, r2)), SHR(x, s3))


def MAJ(x: list, y: list, z: list): 
    res = []
    for _x, _y, _z in zip(x, y, z):
        k = (_x & _y) ^ (_x & _z) ^ (_y & _z)
        res.append(k)
    return res
