#!/usr/bin/env python3
from colorama import Fore, Style

def main():
    print("-----------------Key Commands Menu---------------------\n")
    print("Press 'r' or '1' to change the pencil color to" + Fore.RED + " red.\n" + Style.RESET_ALL)
    print("Press 'g' or '2' to change the pencil color to" + Fore.GREEN + " green.\n" + Style.RESET_ALL)
    print("Press 'b' or '3' to change the pencil color to" + Fore.BLUE + " blue.\n" + Style.RESET_ALL)
    print("Press 'y' or '4' to change the pencil color to" + Fore.YELLOW + " yellow.\n" + Style.RESET_ALL)
    print("Press '+' to increase the pencil line thickness.\n")
    print("Press '-' to decrease the pencil line thickness.\n")
    print("Press 'c' to clean the canvas.\n")
    print("Press 'w' to save the drawing/painting.\n")
    print("------------------------------------------------------\n")

    pass

if __name__ == "__main__":
    main()