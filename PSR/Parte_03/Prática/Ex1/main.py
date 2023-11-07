#!/usr/bin/env python3

import math
from time import time, ctime
import time
import colorama

maximum_number = 50000000


def main():

    tic = time.time()

    print("This is Ex1 and the current date is: " + str(ctime()))

    for n in range(0, maximum_number+1):
        result = math.sqrt(n)
        

    toc = time.time()
    elapsed_time = (toc - tic)

    print("The elapsed time was:", elapsed_time, "seconds.")

    

if __name__ == "__main__":
    main()