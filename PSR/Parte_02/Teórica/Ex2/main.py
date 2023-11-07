#!/usr/bin/env python3

#alternative 1
#import my_functions

#alternative 2
from my_functions import isPerfect


maximum_number = 50 # maximum number to test. this is a global variable

def main():
    #write the code...
    print("Testing for perfect numbers!" )

    for number in range(1, maximum_number+1):
        print("Analyzing number " + str (number))

        if isPerfect(number):
            print(str(number) + " is perfect!")
        else:
            print(str(number) + " is not perfect!")


if __name__ == "__main__":
    main()