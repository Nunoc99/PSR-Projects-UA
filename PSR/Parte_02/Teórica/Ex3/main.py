#!/usr/bin/env python3

import argparse #import argparse library

from my_functions import isPerfect


#maximum_number = 2 # maximum number to test. this is a global variable

def main():
    #write the code...

    parser = argparse.ArgumentParser(description='Test for PSR.')
    parser.add_argument('--maximum_number', type=int, required=True, help='The maximum number until which we check if numbers are perfect')
    
    args = vars(parser.parse_args())
    print(args)
    maximum_number = args["maximum_number"]


    print("Testing for perfect numbers!" )

    for number in range(1, maximum_number+1):
        print("Analyzing number " + str (number))

        if isPerfect(number):
            print(str(number) + " is perfect!")
        else:
            print(str(number) + " is not perfect!")


if __name__ == "__main__":
    main()