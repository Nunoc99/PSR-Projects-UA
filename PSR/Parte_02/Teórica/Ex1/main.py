#!/usr/bin/env python3

maximum_number = 50 # maximum number to test. this is a global variable

def getDividers(number):
    
    dividers = []
    for i in range (1, number):
        if number%i == 0:  #número módulo de i, devolve o resto da divisão inteira
            #print(str(i) + " is an integer divider of " + str(number))
            dividers.append(i)

    #print(str(number) + " has dividers " + str(dividers))
    return dividers


def isPerfect(number):
    "Returns True if number is perfect, False otherwise"

    dividers = getDividers(number)
    
    total = sum(dividers)

    if total == number:
        return True
    else:
        return False


    return True #assume all numbers are perfect

def main():
    #write the code...
    print("Testing for perfect numbers!")

    for number in range(1, maximum_number+1):
        print("Analyzing number " + str (number))

        if isPerfect(number):
            print(str(number) + " is perfect!")
        else:
            print(str(number) + " is not perfect!")


if __name__ == "__main__":
    main()