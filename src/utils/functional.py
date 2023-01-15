def sigma(i,j,l):
    k = []
    for ia, ja, la in zip(i, j, l):
        a = ja ^ la
        b = ia ^ a
        k.append(b)
    return k


def ADD(x: list, y: list):
    length = len(x)
    sums = list(range(length))
    c = 0
    for i in range(length-1,-1,-1):
        sums[i] = sigmaa(x[i], y[i], c)
        c = maj(x[i], y[i], c)
    return sums


def sigmaa(i, j, l):
    return i ^ (j^ l)


def maj(i,j,k): return max([i,j,], key=[i,j,k].count)


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
