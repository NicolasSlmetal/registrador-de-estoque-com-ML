import random

# Geração de código


def gerarcod():
    cc = CodeGenerator()
    code = ""
    c = 0
    while len(code) < 10:
        if c % 2 == 0:
            code += random.choice(cc.alpha)
        else:
            code += str(random.randint(0, 9))
        c += 1
    return code


class CodeGenerator:

    def __init__(self):
        self.alpha = ["A", "B", "C", "D", "E", "F"
                      , "G", "H", "I", "J", "K", "L",
                      "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
                      "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"
                      , "l", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "o", "p",
                       "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

