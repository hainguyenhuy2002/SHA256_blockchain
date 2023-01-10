from stdio import inputs, wait_for, Action, set_property

__space__ = 7

def set_space(space):
    global __space__
    __space__ = space


def get_space():
    global __space__
    return __space__


def show(name, *val, end='\n'):
    space = max(get_space(), len(name))
    name = Action.LINE_RIGHT * (space - len(name)) + name
    print(Action.LINE_CLEAR + name, *val, end=end)    


def shr(x="11111111000000001111111100000000", r=32, show_first=True, line_up=1, space=None, postfix=""):
    shift = x[::]

    if space is not None:
        set_space(space)
    if show_first:
        show("X", x)
        show("SHR " + str(r), shift, postfix)

    for _ in range(r):
        wait_for()
        shift = '0' + shift[:-1]

        set_property(Action.LINE_UP * line_up)
        show("SHR " + str(r), shift, postfix, end='\n' * line_up)
    return shift


def rotr(x="11111111000000001111111100000000", r=32, show_first=True, line_up=1, space=None, postfix=""):
    shift = x[::]

    if space is not None:
        set_space(space)
    if show_first:
        show("X", x)
        show("ROTR " + str(r), shift, postfix)

    for _ in range(r):
        wait_for()
        shift = shift[-1] + shift[:-1]

        set_property(Action.LINE_UP * line_up)
        show("ROTR " + str(r), shift, postfix, end='\n' * line_up)
    return shift
    

def sigma0(x="00000000000000000011111111111111", r1=7, r2=18, r3=3):
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


def choice(x, y, z):
    pass


if __name__ == "__main__":
    # shr(space=6, r=16)
    # rotr(space=7, r=4)
    sigma0()
