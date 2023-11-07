
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


if __name__ == "__main__":
    main()