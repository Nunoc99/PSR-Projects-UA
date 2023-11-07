#!/usr/bin/env python3

from readchar import readkey

def printAllPreviousChars():

    stop_character = readkey()
    stop_number = ord(stop_character)

    print("Printing all chars up to: " + str(stop_character))

    characters = []
    for n in range (32, stop_number):
        character = chr(n)
        characters.append(character)

    print(characters)
    print("The ASCII value of " + str(stop_character)+ " is " + str(stop_number))




def main():

    #4a
    printAllPreviousChars()

    #4b 
    #readAllUpTo(stop_char)

    #4c 
    #countNumbersUpto(stop_char)



if __name__ == "__main__":
    main()