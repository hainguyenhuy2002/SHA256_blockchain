from typing

def sigma(i,j,l):
    k = []
    for ia, ja, la in zip(i, j, l):
        a = ja ^ la
        b = ia ^ a
        k.append(b)
    return k


def NOT(j):
    k = []
    for i in j:
        if i == 1:
            k.append(0)
        if i == 0:
            k.append(1)
    return k


def AND(i, j):
    k = []
    for ia, ja in zip(i, j):
        a = ia & ja
        k.append(a)
    return k


def XOR(i, j): 
    k = []
    for ia, ja in zip(i, j):
        a = ia ^ ja
        k.append(a)
    return k


def add(i, j):
    length = len(i)
    sums = list(range(length))
    c = 0
    for x in range(length-1,-1,-1):
        sums[x] = sigmaa(i[x], j[x], c)
        c = maj(i[x], j[x], c)
    return sums


def maj(i,j,k): return max([i,j,], key=[i,j,k].count)

def rotr(x, n): return x[-n:] + x[:-n]

def shr(x, n): return n * [0] + x[:-n]

def isTrue(x): return x == 1

def if_(i, y, z): return y if isTrue(i) else z

def not_(i): return if_(i, 0, 1)

def xor(i, j): return if_(i, not_(j), j)

def sigmaa(i, j, l): return xor(i, xor(j, l))


def SIGMA(x: )
