import keyboard

# ANSI
class Action:
    LINE_UP = '\033[1A'
    LINE_DOWN = '\n'
    LINE_RIGHT = '\033[1C'
    LINE_LEFT = '\033[1D'
    LINE_CLEAR = '\x1b[2K'


class Symbol:
    TRIANGLE_RIGHT = chr(16)
    TRIANGLE_LEFT = chr(17)
    TRIANGLE_UP = chr(30)
    TRIANGLE_DOWN = chr(31)
    

class Color:
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    YELLOW = "\033[1;33m"
    WHITE = "\033[1;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_GRAY = "\033[0;37m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"


class Style:
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"


class Default:
    END = "\033[0m"


def set_property(*prop):
    print(*prop, end="", sep="")


def inputs(msg: str=None):
    __msg = "(Ctrl-Z + Enter to leave input mode)"
    print(msg + " " + __msg if msg is not None else __msg)
    lines = []
    while True:
        try:
            lines.append(input())
        except EOFError:
            break
    return "\n".join(lines)


def wait_for(key='enter'):
    keyboard.wait(key)
    print(Action.LINE_UP, end="")
    input()
    print(end=Action.LINE_CLEAR)


if __name__ == "__main__":
    set_property(Color.RED)
    print("red line")
    
    set_property(Style.BOLD)
    print("red bold line")

    set_property(Default.END)
    print("back to default")

    set_property(Color.CYAN, Style.ITALIC)
    import time
    for i in range(8):
        print(i, 'italic')
        time.sleep(0.5)

        if i % 3 == 2:
            set_property(Action.LINE_UP * 3)

    # print()
    # print("Wait for enter")
    # wait_for_enter()
    # print(inputs("Input text here:"))

    # print("111111111111111111111111111111111")
    # print("222222222222222222222222222222222")
    # print("333333333333333333333333333333333")
    # print("444444444444444444444444444444444")
    # print(Action.LINE_UP * 3)
    # print()

    # set_property(Color.RED, Style.BOLD)
    # print(input())

    # wait_for_enter()
    # print("first wait")
    # wait_for_enter()
    # wait_for_enter()
    # print("done")
