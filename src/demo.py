from stdio import inputs, wait_for, Action, Symbol, set_property
from typing import Union


__space__ = 7

def set_space(space):
    global __space__
    __space__ = space


def get_space():
    global __space__
    return __space__


def show(name, *val, line_up=0):
    space = max(get_space(), len(name))
    set_property(Action.LINE_UP * line_up)
    name = Action.LINE_RIGHT * (space - len(name)) + name
    print(Action.LINE_CLEAR + name, *val, end='\n' * max(1, line_up))    


def int2bin(value, num_bits=32):
    if isinstance(value, int):
        b = bin(value).replace('0b', "")
        b = '0' * (num_bits - len(b)) + b
        return b
    else:
        raise ValueError("type of value must be int, not" + str(type(value)))


def check(x: Union[int, str]):
    x = int2bin(x) if isinstance(x, int) else x
    assert len(x) == 32
    return x


def shr(x: Union[int, str]="11111111000000001111111100000000", r=32, show_first=True, line_up=1, space=None, postfix=""):
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


def rotr(x: Union[int, str]="11111111000000001111111100000000", r=32, show_first=True, line_up=1, space=None, postfix=""):
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
    

def sigma0(x: Union[int, str]="00000000000000000011111111111111", r1=7, r2=18, r3=3):
    x = check(x)

    set_space(9)
    show('X', x)
    show("ROTR " + str(r1), x)
    show("ROTR " + str(r2), x, "XOR")
    show("SHR "  + str(r3), x, "XOR")
    show("", "--------------------------------")
    show("sigma0(x)")

    rotr_1  = rotr(x, r=r1, show_first=False, line_up=5)
    rotr_2  = rotr(x, r=r2, show_first=False, line_up=4, postfix="XOR")
    shr_3   = shr( x, r=r3, show_first=False, line_up=3, postfix='XOR')

    res = [' ' for _ in range(32)]
    for i in range(31, -1, -1):
        res[i] = str(int(rotr_1[i]) ^ int(rotr_2[i]) ^ int(shr_3[i]))
        wait_for()
        set_property(Action.LINE_UP)
        show("sigma0(x)", "".join(res))


def ch(x: Union[int, str], y: Union[int, str], z: Union[int, str]):
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
        

def maj(x: Union[int, str], y: Union[int, str], z: Union[int, str]):
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


def hash():
    print("| Message:")
    msg = input("Input your message: ")
    msg_bytes = [ord(c) for c in msg]
    print      ("Bytes:            ", msg_bytes)
    msg = "".join([int2bin(i, 8) for i in msg_bytes])
    print      ("Message:          ", msg)
    print()

    wait_for()

    if len(msg) < 448:
        set_space(0)
        
        def show_msg(first=False, old_bits=None):
            first = int(not first)
            bits = lambda num: f"{num} bits" if num > 1 else f"{num} bit"
            
            if old_bits is None:
                __m = f"({bits(len(msg))})"
            else:
                __m = f"({bits(old_bits)} -> {bits(len(msg))})"

            show("| Padding:", __m, line_up=2 * first)
            show("Message:", msg, line_up=1 * first)

        show_msg(True)
        wait_for()

        msg += '1'
        show_msg(old_bits=len(msg) - 1)
        wait_for()

        __len = len(msg)
        msg += '0' * (448 - len(msg))
        show_msg(old_bits=__len)
        wait_for()




    elif len(msg) <= 512:
        pass
    else:
        pass






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

    hash()