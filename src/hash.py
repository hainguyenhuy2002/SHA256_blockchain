from utils.functional import *
from utils.constants import *
from utils.process import *

def sha256(message): 
    k = initializer(K)
    h0, h1, h2, h3, h4, h5, h6, h7 = initializer(h_hex)
    chunks = preprocessMessage(message)
    for chunk in chunks:
        w = chunker(chunk, 32)
        for _ in range(48):
            w.append(32 * [0])
        for i in range(16, 64):
            s0 = sigma(ROTR(w[i-15], 7), ROTR(w[i-15], 18), SHR(w[i-15], 3) ) 
            s1 = sigma(ROTR(w[i-2], 17), ROTR(w[i-2], 19), SHR(w[i-2], 10))
            w[i] = ADD(ADD(ADD(w[i-16], s0), w[i-7]), s1)
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7
        for j in range(64):
            S1 = sigma(ROTR(e, 6), ROTR(e, 11), ROTR(e, 25) )
            ch = XOR(AND(e, f), AND(NOT(e), g))
            temp1 = ADD(ADD(ADD(ADD(h, S1), ch), k[j]), w[j])
            S0 = sigma(ROTR(a, 2), ROTR(a, 13), ROTR(a, 22))
            m = sigma(AND(a, b), AND(a, c), AND(b, c))
            temp2 = ADD(S0, m)
            h = g
            g = f
            f = e
            e = ADD(d, temp1)
            d = c
            c = b
            b = a
            a = ADD(temp1, temp2)
        h0 = ADD(h0, a)
        h1 = ADD(h1, b)
        h2 = ADD(h2, c)
        h3 = ADD(h3, d)
        h4 = ADD(h4, e)
        h5 = ADD(h5, f)
        h6 = ADD(h6, g)
        h7 = ADD(h7, h)
    digest = ''
    for val in [h0, h1, h2, h3, h4, h5, h6, h7]:
        digest += binToHexa(val)
    return digest

if __name__ == '__main__':
    verdict = 'yes'
    while verdict == 'yes':
        input_message = input('Type or copy your message here: ')
        print('Your message: ', input_message)
        print('Hash: ', sha256(input_message))
        verdict = input('Do you want to try another text? (yes/no): ').lower()