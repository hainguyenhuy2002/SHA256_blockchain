from subprocess import list2cmdline
from stdio import inputs, wait_for, Action, Symbol, set_property
from typing import Union
import math
from functools import partial
from utils.functional import *
from utils.constants import *
from utils.process import *



__space__ = 7

def set_space(space):
    global __space__
    __space__ = space


def get_space():
    global __space__
    return __space__


def show(name, *val, line_up=0, space_right=False):
    space = max(get_space(), len(name))
    set_property(Action.LINE_UP * line_up)
    if space_right is False:
        name = Action.LINE_RIGHT * (space - len(name)) + name
    else:
        name += ' ' * (space - len(name))
    print(Action.LINE_CLEAR + name, *val, end='\n' * max(1, line_up))    


def int2bin(value, num_bits=32):
    if isinstance(value, int):
        b = bin(value).replace('0b', "")
        b = '0' * (num_bits - len(b)) + b
        return b
    else:
        raise ValueError("type of value must be int, not" + str(type(value)))


def str2list(bin):
    return [int(i) for i in bin]


def list2str(_list):
    return "".join([str(l) for l in _list])


def check(x: Union[int, str]):
    x = int2bin(x) if isinstance(x, int) else x
    assert len(x) == 32
    return x


def shr_demo(x: Union[int, str]="11111111000000001111111100000000", r=32, show_first=True, line_up=1, space=None, postfix=""):
    x = check(x)
    shift = x[::]

    if space is not None:
        set_space(space)
    if show_first:
        show("X", x)
        show("SHR " + str(r), shift, postfix)

    for _ in range(r):
        wait_for()
        shift = '0' + shift[:-1]

        show("SHR " + str(r), shift, postfix, line_up=line_up)
    return shift


def rotr_demo(x: Union[int, str]="11111111000000001111111100000000", r=32, show_first=True, line_up=1, space=None, postfix=""):
    x = check(x)
    shift = x[::]

    if space is not None:
        set_space(space)
    if show_first:
        show("X", x)
        show("ROTR " + str(r), shift, postfix)

    for _ in range(r):
        wait_for()
        shift = shift[-1] + shift[:-1]

        show("ROTR " + str(r), shift, postfix, line_up=line_up)
    return shift
    

def sigma_demo(x: Union[int, str]="00000000000000000011111111111111", r1=7, r2=18, r3=3):
    x = check(x)

    set_space(8)
    show('X', x)
    show("ROTR " + str(r1), x)
    show("ROTR " + str(r2), x, "XOR")
    show("SHR "  + str(r3), x, "XOR")
    show("", "--------------------------------")
    show("sigma(x)")

    rotr_1  = rotr_demo(x, r=r1, show_first=False, line_up=5)
    rotr_2  = rotr_demo(x, r=r2, show_first=False, line_up=4, postfix="XOR")
    shr_3   = shr_demo( x, r=r3, show_first=False, line_up=3, postfix='XOR')

    res = [' ' for _ in range(32)]
    for i in range(31, -1, -1):
        res[i] = str(int(rotr_1[i]) ^ int(rotr_2[i]) ^ int(shr_3[i]))
        wait_for()
        set_property(Action.LINE_UP)
        show("sigma(x)", "".join(res))


def ch_demo(x: Union[int, str], y: Union[int, str], z: Union[int, str]):
    x = check(x)
    y = check(y)
    z = check(z)

    set_space(1)
    print()
    show("X", x)
    show("Y", y)
    show("Z", z)
    show("", "--------------------------------")
    print()

    res     = [' ' for _ in range(32)]
    cursor  = [' ' for _ in range(33)]

    for i in range(31, -1, -1):
        wait_for()
        
        if x[i] == '1':
            res[i] = y[i]
            postfix = [" ", Action.LINE_LEFT + Symbol.TRIANGLE_LEFT]
        else:
            res[i] = z[i]
            postfix = [Action.LINE_LEFT + Symbol.TRIANGLE_LEFT, " "]

        cursor[i + 1] = ' '
        cursor[i] = Symbol.TRIANGLE_DOWN

        show("", "".join(cursor), line_up=6)
        show("Y", y, postfix[0], line_up=4)
        show("Z", z, postfix[1], line_up=3)
        show("", "".join(res), line_up=1)
    return res
        

def maj_demo(x: Union[int, str], y: Union[int, str], z: Union[int, str]):
    x = check(x)
    y = check(y)
    z = check(z)

    set_space(1)
    show("X", x)
    show("Y", y)
    show("Z", z)
    show("", "--------------------------------")
    print()

    res = [' ' for _ in range(32)]
    for i in range(31, -1, -1):
        wait_for('enter')

        _x = int(x[i])
        _y = int(y[i])
        _z = int(z[i])
        res[i] = str((_x & _y) ^ (_x & _z) ^ (_y & _z))

        show("", "".join(res), line_up=1)
    return res


def input_msg():
    print("--------------------------------------------------------------------------------")
    print("Message:")
    print("--------------------------------------------------------------------------------")
    msg = input("Input your message: ")
    msg_bytes = [ord(c) for c in msg]
    print      ("Bytes:             ", msg_bytes)
    msg_bytes = "".join([int2bin(i, 8) for i in msg_bytes])
    print      ("Message:           ", msg_bytes)
    return msg, msg_bytes


def padding(msg):
    def show_msg(old_bits=None):
        bits = lambda num: f"{num} bits" if num > 1 else f"{num} bit"
        bits_per_line = 64
        
        if old_bits is None:
            old_bits = 0
            __m = f"({bits(len(msg))})"
        else:
            __m = f"({bits(old_bits)} -> {bits(len(msg))})"

        num_old_lines = math.ceil(old_bits / bits_per_line)
        set_property(Action.LINE_UP * (num_old_lines + 3))
        print("--------------------------------------------------------------------------------")
        print("Padding:", __m)
        print("--------------------------------------------------------------------------------")

        lines = math.ceil(len(msg) / bits_per_line)
        for i in range(lines):
            line = msg[i * bits_per_line : min(len(msg), (i + 1) * bits_per_line)]
            if i == 0:
                print("Message:      ", line)
            else:
                print("              ", line)

    wait_for()
    print("\n\n\n")
    show_msg()        

    if len(msg) < 448: 
        old_len = len(msg)
        wait_for()
        msg += '1'
        show_msg(old_bits=len(msg) - 1)

        wait_for()
        __len = len(msg)
        msg += '0' * (448 - len(msg))
        show_msg(old_bits=__len)

        wait_for()
        msg += int2bin(old_len, 64)
        show_msg(old_bits=448)

    elif len(msg) <= 512:
        old_len = len(msg)
        wait_for()
        msg += '1'
        show_msg(old_bits=len(msg) - 1)

        wait_for()
        __len = len(msg)
        msg += '0' * (1024 - 64 - len(msg))
        show_msg(old_bits=__len)

        wait_for()
        msg += int2bin(old_len, 64)
        show_msg(old_bits=1024 - 64)
    else:
        old_len = len(msg)
        wait_for()
        msg += '1'
        show_msg(old_bits=len(msg) - 1)

        wait_for()
        __len = len(msg)
        __new_len = math.ceil(__len / 512) * 512 - 64
        msg += '0' * (__new_len - len(msg))
        show_msg(old_bits=__len)

        wait_for()
        msg += int2bin(old_len, 64)
        show_msg(old_bits=__new_len)

    wait_for()
    bits_per_line = 64
    lines = math.ceil(len(msg) / bits_per_line)
    for i in range(lines):
        line = msg[i * bits_per_line : min(len(msg), (i + 1) * bits_per_line)]
        if i == 0:
            print("\nMessage block:", line)
        else:
            print("              ", line)

    msgs = []
    chunk_len = 512
    for i in range(0, len(msg), chunk_len):
        msgs.append(msg[i : i + chunk_len])
    return msgs


def message_scheduler(msg):
    wait_for()
    print("\n--------------------------------------------------------------------------------")
    print("Message scheduler:")
    print("--------------------------------------------------------------------------------")
    set_space(3)
    ws = [msg[i * 32: (i + 1) * 32] for i in range(16)]

    def show_ws(n_last, use_postfix=True, line_up=0, **kwargs):
        set_property(Action.LINE_UP * line_up)
        show_r = partial(show, space_right=True)

        for idx, w in enumerate(ws[-n_last:]):
            idx_ = idx + len(ws) - n_last
            if use_postfix is False:
                show_r(f"W{idx_}", w)
            elif idx == 0:
                show_r(f"W{idx_}", w, "->       ", w)
            elif idx == 1:
                show_r(f"W{idx_}", w, "-> sigma0", kwargs['sigma0'])
            elif idx == 9:
                show_r(f"W{idx_}", w, "->       ", w)
            elif idx == 14:
                show_r(f"W{idx_}", w, "-> sigma1", kwargs['sigma1'])
            elif idx == 16:
                show_r(f"W{idx_}", w, "= sigma1(t-2) + (t-7) + sigma0(t-15) + (t-16)")
            else:
                show_r(f"W{idx_}", w)

    show_ws(16, False)

    for i in range(16, 64):
        wait_for()
        sigma0 = SIGMA(str2list(ws[i - 15]), 7, 18, 3)
        sigma1 = SIGMA(str2list(ws[i - 2]), 17, 19, 10)
        w = ADD(sigma1, str2list(ws[i - 7]))
        w = ADD(w, sigma0)
        w = ADD(w, str2list(ws[i - 16]))
        ws.append(list2str(w))

        show_ws(17, line_up=min(17, i), sigma0=list2str(sigma0), sigma1=list2str(sigma1))

    wait_for()
    show_ws(17, False, line_up=17)

    return ws

def compression(ws, is_first, is_final, hs: list=None):
    wait_for()
    def show_value(value_n_last, T_n_last =2 ,step= 0,lineup = 0, multiple =False, index = 0, isFrist=False ,substep =0,end =False,**kwargs):
        set_property(Action.LINE_UP * lineup)
        show_r = partial(show, space_right=True)
        ### first step
        if step == 0:
            print("--------------------------------------------------------------------------------")
            show_r("Compression: H0 (Initial hash)")
            print("--------------------------------------------------------------------------------")
    
            for idx, v in enumerate(hash_value[-value_n_last:]):
                if multiple:
                    show_r(value[idx], "=", v, "* 2 ^ 32")
                else:
                    show_r(value[idx], "=", v)

        elif step ==1:
            print("--------------------------------------------------------------------------------")
            show_r("Compression: H0 ---> H1")
            print("--------------------------------------------------------------------------------")
            show_r(f"W{index}", " =", ws[index], " (message schedule)")
            show_r(f"K{index}", " =", k_demo[index], " (constant)")
            print(" ")
            for idx, v in enumerate( T_list[-T_n_last:]):
                if idx == 0:
                    show_r("T1  = Σ1(e) + Ch(e, f, g) + h + ",f"K{index}"," + ",f"W{index}"," = ", v)
                else:
                    show_r("T2  = Σ0(a) + Maj(a, b, c) = ", v)
                    
            for idx, v in enumerate(hash_value[-value_n_last:]):
                if isFrist:
                    show_r(value[idx], "=", v)
                
                else:    
                    if idx %8 == 0:
                        show_r(value[idx], "=", v,"<- T1 + T2")
                    elif idx %8 == 4:
                        show_r(value[idx], "=", v," + T1 ")
                    else:
                        show_r(value[idx], "=", v)
        
        elif step == 2:
            print("                                                                                ")   
            print("                                                                                ")            
            print("                                                                                ")
            print("--------------------------------------------------------------------------------")
            show_r("Compression: H1")
            print("--------------------------------------------------------------------------------")
            print("                                                                                ")
            print("                                                                                ")

            for idx, v in enumerate( value[-value_n_last:]):
                if substep ==0:
                    show_r(value[idx], "=", previous_hash_value_list[idx], "+ ", after_hash_value_list[idx])
                elif substep ==1:
                    show_r(value[idx], "=", final_hash_value_list[idx])
                elif substep ==2:
                    show_r(value[idx], "=", final_hash_value_list[idx]+ "->" + hex_hash_value_list[idx])
            if end == True: 
                show_r("final result: ", digest)
                pass

            # show_r(ws[i])

    k_list = initializer(K)  #list
    
    if is_first:
        show_value(8)
        wait_for()

        for i in sqrt_prime:
            hash_value.append(i)
        show_value(8,lineup= 11)
        wait_for()

        sqrt_list = []
        dec_list = []
        for i in prime_list:
            a = round(math.sqrt(i), 10)
            b = round(a - int(a), 10)
            sqrt_list.append(a)
            dec_list.append(b)
        for i in sqrt_list:
            hash_value.append(i)
        show_value(8,lineup= 11)
        wait_for()

        for j in dec_list:
            hash_value.append(j)
        show_value(8,lineup= 11)
        wait_for()

        # for k in dec_list:
        #     hash_value.append(k)
        show_value(8,lineup= 11 ,multiple=True)
        wait_for()

        for i in initializer(h_hex):
            k = list2str(i) 
            hash_value.append(k)
        show_value(8,lineup= 11)
        wait_for()

    #######################
        a, b, c, d, e, f, g, h = hash_value[-8:] #string  
        hs = hash_value[-8:] #string  
        
    h0 = str2list(hs[0])
    h1 = str2list(hs[1])
    h2 = str2list(hs[2])
    h3 = str2list(hs[3])
    h4 = str2list(hs[4])
    h5 = str2list(hs[5])
    h6 = str2list(hs[6])
    h7 = str2list(hs[7])
    a = h0
    b = h1
    c = h2
    d = h3
    e = h4
    f = h5
    g = h6
    h = h7

    k_demo = []
    # a0, b0, c0, d0, e0, f0, g0, h0, T1_0, T2_0 = compression_algorithm(a,b,c,d,e,f,g,h,0)
    # list0 = ['',list2str(b0),list2str(c0),list2str(d0),list2str(d0), list2str(f0), list2str(g0),list2str(h0)]
    # for i in list0:
    #     hash_value.append(i)
    
    previous_hash_value_list =  [list2str(a), list2str(b),list2str(c),list2str(d),list2str(e),list2str(f),list2str(g),list2str(h)]
    for i in range(64):
        k_demo.append(list2str(k_list[i])) 
        #wc
        if i ==0:
            show_value(value_n_last=8,step=1,lineup=16,index = i, isFrist=True)
            wait_for()
        w = str2list(ws[i])   
        S1 = sigma(ROTR(e, 6), ROTR(e, 11), ROTR(e, 25) )
        ch = XOR(AND(e, f), AND(NOT(e), g))
        T1 = ADD(ADD(ADD(ADD(h, S1), ch), k_list[i]), w)
        S0 = sigma(ROTR(a, 2), ROTR(a, 13), ROTR(a, 22))
        m = sigma(AND(a, b), AND(a, c), AND(b, c))
        T2 = ADD(S0, m)
        T_list.append(list2str(T1))
        T_list.append(list2str(T2))
        if i ==0:
            show_value(value_n_last=8,step=1,lineup=16,index = i, isFrist=True)
            wait_for()
        else:
            show_value(value_n_last=8,step=1,lineup=16,index = i)
            wait_for()

        h = g
        g = f
        f = e
        e = ADD(d, T1)
        d = c
        c = b
        b = a
        a = ADD(T1, T2)
        
        list1 = ['                                ',list2str(b),list2str(c),list2str(d),list2str(d), list2str(f), list2str(g),list2str(h)]        
        for j in list1:
            hash_value.append(j)
        if i ==0:
            show_value(value_n_last=8,step=1,lineup=16,index = i, isFrist=True)
            wait_for()
            show_value(value_n_last=8,step=1,lineup=16,index = i)
            wait_for()
        else:
            show_value(value_n_last=8,step=1,lineup=16,index = i)
            wait_for()

        
        list2 = [list2str(a),list2str(b),list2str(c),list2str(d),list2str(d), list2str(f), list2str(g),list2str(h)] 
        for j in list2:
            hash_value.append(j)
        
        show_value(value_n_last=8,step=1,lineup=16,index = i)
        wait_for()

        list3 = [list2str(a),list2str(b),list2str(c),list2str(d),list2str(e), list2str(f), list2str(g),list2str(h)] 
        for j in list3:
            hash_value.append(j)
        show_value(value_n_last=8,step=1,lineup=16,index = i)
        wait_for()
        #a b c d e f g h
    after_hash_value_list =  [list2str(a), list2str(b),list2str(c),list2str(d),list2str(e),list2str(f),list2str
    (g),list2str(h)]
    show_value(value_n_last=8,step=2,lineup=16)
    wait_for()


    h0 = ADD(h0, a)
    h1 = ADD(h1, b)
    h2 = ADD(h2, c)
    h3 = ADD(h3, d)
    h4 = ADD(h4, e)
    h5 = ADD(h5, f)
    h6 = ADD(h6, g)
    h7 = ADD(h7, h)
    final_hash_value_list = [list2str(h0), list2str(h1),list2str(h2),list2str(h3),list2str(h4),list2str(h5),list2str(h6),list2str(h7)]
    show_value(value_n_last=8,step=2,substep=1,lineup=16)
    wait_for()

    if is_final:
        hex_hash_value_list = []
        digest = ''
        for val in [h0, h1, h2, h3, h4, h5, h6, h7]:
            digest += binToHexa(val)
            hex_hash_value_list.append(binToHexa(val))
        show_value(value_n_last=8,step=2,substep=2,lineup=16)
        wait_for()
        show_value(value_n_last=8,step=2,substep=2, end=True,lineup=16)
        wait_for()

        return digest
    return [h0, h1, h2, h3, h4, h5, h6, h7]
        

def hash_demo():
    raw_msg, msg = input_msg()
    msgs = padding(msg)
    hs = None
    for idx, msg in enumerate(msgs):
        ws = message_scheduler(msg)
        hs = compression(ws, is_first=(idx == 0), is_final=(idx == len(msgs) - 1), hs=hs)
    return raw_msg

        
if __name__ == "__main__":
    # shr_demo(space=6, r=16)

    # rotr(space=7, r=4)

    #sigma_demo(x = "00000000000000000011111111111111")

    # ch_demo(
    #     x="00000000111111110000000011111111",
    #     y="00000000000000001111111111111111",
    #     z="11111111111111110000000000000000"
    # )

    # maj(
    #     x="01010000000100101010101000001010",
    #     y="00100010010100010101000010100001",
    #     z="00101000000101010111111110101111"
    # )

    input = hash_demo()
    print(input)
    import hashlib
    print(hashlib.sha256(input.encode('utf-8')).hexdigest())

   