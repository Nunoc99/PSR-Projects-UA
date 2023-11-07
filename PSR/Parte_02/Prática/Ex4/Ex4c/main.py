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
    


def readAllUpTo(stop_char):

    while True:
        k = readkey()
        print("You entered character: " + str(k))

        if k==stop_char:
            break

        

def countNumbersUpto(stop_char):

    inputs = []
    input_numbers = []
    input_others = []


    while True:
        k = readkey()
        print("You entered a character: " + str(k))

        if k==stop_char:
            break
        inputs.append(k)


    #alternativa para o ciclo FOR
    #input_numbers = [input for inputs in inputs if input.isnumeric()]
    #input_others = [input for inputs in inputs if not input.isnumeric()]
        

    for input in inputs:
        if input.isnumeric():
            input_numbers.append(input)
        else:
            input_others.append(input)

        
    total_numbers = len(input_numbers) 
    total_others = len(input_others)

    print("You entered " + str(total_numbers) + " numbers.")
    print("You entered " + str(total_others) + " others.")



def main():

    #4a
    #printAllPreviousChars()

    #4b
    #readAllUpTo("X")

    #4c 
    countNumbersUpto("X")



if __name__ == "__main__":
    main()