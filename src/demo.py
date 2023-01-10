from stdio import inputs, wait_for, Action, Symbol, set_property
from typing import Union
import math
from utils.functional import SIGMA, ADD 
from functools import partial


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

    set_space(9)
    show('X', x)
    show("ROTR " + str(r1), x)
    show("ROTR " + str(r2), x, "XOR")
    show("SHR "  + str(r3), x, "XOR")
    show("", "--------------------------------")
    show("sigma0(x)")

    rotr_1  = rotr_demo(x, r=r1, show_first=False, line_up=5)
    rotr_2  = rotr_demo(x, r=r2, show_first=False, line_up=4, postfix="XOR")
    shr_3   = shr_demo( x, r=r3, show_first=False, line_up=3, postfix='XOR')

    res = [' ' for _ in range(32)]
    for i in range(31, -1, -1):
        res[i] = str(int(rotr_1[i]) ^ int(rotr_2[i]) ^ int(shr_3[i]))
        wait_for()
        set_property(Action.LINE_UP)
        show("sigma0(x)", "".join(res))


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
    print("| Message:")
    msg = input("Input your message: ")
    msg_bytes = [ord(c) for c in msg]
    print      ("Bytes:             ", msg_bytes)
    msg = "".join([int2bin(i, 8) for i in msg_bytes])
    print      ("Message:           ", msg)
    print()
    return msg


def padding(msg):
    wait_for()

    def show_msg(old_bits=None):
        bits = lambda num: f"{num} bits" if num > 1 else f"{num} bit"
        bits_per_line = 64
        
        if old_bits is None:
            old_bits = 0
            __m = f"({bits(len(msg))})"
        else:
            __m = f"({bits(old_bits)} -> {bits(len(msg))})"

        num_old_lines = math.ceil(old_bits / bits_per_line)
        set_property(Action.LINE_UP * (num_old_lines + 1))
        print("| Padding:", __m)

        lines = math.ceil(len(msg) / bits_per_line)
        for i in range(lines):
            line = msg[i * bits_per_line : min(len(msg), (i + 1) * bits_per_line)]
            if i == 0:
                print("Message:        ", line)
            else:
                print("                ", line)

    if len(msg) < 448:    
        print()
        show_msg()

        wait_for()
        msg += '1'
        show_msg(old_bits=len(msg) - 1)

        wait_for()
        __len = len(msg)
        msg += '0' * (448 - len(msg))
        show_msg(old_bits=__len)

        wait_for()
        msg += int2bin(__len, 64)
        show_msg(old_bits=448)

    elif len(msg) <= 512:
        pass
    else:
        pass

    wait_for()
    bits_per_line = 64
    lines = math.ceil(len(msg) / bits_per_line)
    for i in range(lines):
        line = msg[i * bits_per_line : min(len(msg), (i + 1) * bits_per_line)]
        if i == 0:
            print("\n| Message block:", line)
        else:
            print("                ", line)
    return msg


def message_scheduler(msg):
    wait_for()
    print("\n| Message scheduler:")
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
        w = ADD(sigma1, str2list(ws[i-7]))
        w = ADD(w, sigma0)
        w = ADD(w, str2list(ws[i-16]))
        ws.append(list2str(w))

        show_ws(17, line_up=min(17, i), sigma0=list2str(sigma0), sigma1=list2str(sigma1))


def hash_demo():
    msg = input_msg()
    msg = padding(msg)
    ws = message_scheduler(msg)

if __name__ == "__main__":
    # shr(space=6, r=16)
    # rotr(space=7, r=4)
    # sigma0()
    # ch(
        # x="00000000111111110000000011111111",
    #     y="00000000000000001111111111111111",
    #     z="11111111111111110000000000000000"
    # )
    # maj(
    #     x="01010000000100101010101000001010",
    #     y="00100010010100010101000010100001",
    #     z="00101000000101010111111110101111"
    # )

    hash_demo()
    # print(list2str(ADD(str2list("0110"), str2list("1011"))))
