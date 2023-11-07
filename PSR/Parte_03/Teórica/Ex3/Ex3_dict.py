#!/usr/bin/env python3

from collections import namedtuple

Complex = namedtuple("Complex", ["r", "i"])

def addComplex(x, y):
    #(a+bi) + (c+di) = (a+c) + (b+d)i

    a = x["r"]
    b = x["i"]
    c = y["r"]
    d = y["i"]

    real = a + c
    imaginary = b + d

    return {"r": real, "i": imaginary}  

def multiplyComplex(x, y):
    #(a+bi)(c+di) = ac + adi + bci + bdi2

    a = x["r"]
    b = x["i"]
    c = y["r"]
    d = y["i"]

    real = a * c - b * d
    imaginary = a * d + b * c

    return {"r": real, "i": imaginary}

def printComplex(x):
    real = x["r"]
    imaginary = x["i"]
    print(str(real) + "+" + str(imaginary) + "i")


def main():
    # ex2 a)

    # define two complex numbers as tuples of size two

    c1 = {"r":5, "i":7}
    c2 = {"r":2, "i":1}
    printComplex(c1)
    printComplex(c2)


    # Test add
    print("Result of addition is: ")
    printComplex(addComplex(c1, c2))

    # test multiply
    print("Result of multiplication is: ")
    printComplex(multiplyComplex(c1, c2))



if __name__ == "__main__":
    main()