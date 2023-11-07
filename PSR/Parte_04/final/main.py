#!/usr/bin/env python3

import time
import random
import argparse
from datetime import date, datetime
from readchar import readkey
from colorama import Fore, Style
from collections import namedtuple
from pprint import pprint


#Definição de Argumentos/help menu
parser = argparse.ArgumentParser(description="Definition of test mode")

parser.add_argument("-utm", "--use_time_mode", help=" Max number of secs for time mode or maximum number of inputs for number of inputs mode.", action="store_true")
parser.add_argument("-mv", "--max_value", help=" Max number of secs for time mode or maximum number of inputs for number of inputs mode.", type=int)            
args = parser.parse_args()

#Variáveis globais
max_value = args.max_value
today = date.today()
today_date = today.strftime("%B %d, %Y")
inputs = namedtuple("Input", ["requested", "received", "duration"])
inputs_array = []



#Modo de tempo máximo
def time_max_mode():
    print(Fore.RED + "PSR", Style.RESET_ALL + "typing test, Rafael & Nuno", today_date)
    print("Test running up to " + str(max_value) + " seconds.")
    print("Press any key to start the test")
    s_key = readkey()
    
    if s_key == s_key:
        test_start = time.time()
        test_start_date = datetime.now()
        test_start_date_txt = test_start_date.strftime("%A %B %d %H:%M:%S %Y")
        number_of_types = 0 
        number_of_hits = 0
        type_sum_duration = 0
        type_hit_sum_duration = 0
        type_miss_sum_duration = 0
        
        while True: 
            random_letter = chr(random.randint(ord('a'), ord('z')))
            key_requested = time.time()
            print("Type letter " + Fore.BLUE + random_letter, Style.RESET_ALL)
            key = readkey()
            key_pressed = time.time()
            duration = (key_pressed - key_requested)
            type_sum_duration += duration
            
            if key == random_letter:
                type_hit_sum_duration += duration
                number_of_hits += 1
                print("You typed letter " + Fore.GREEN + key, Style.RESET_ALL)
            else:
                type_miss_sum_duration += duration
                print("You typed letter " + Fore.RED + key, Style.RESET_ALL)
           
            inputs_add = inputs(random_letter, key, duration)
            inputs_array.append(inputs_add)
            number_of_types +=1
            accuracy = ((number_of_hits / number_of_types) * 100)
            accuracy_dict = str(accuracy) + "%"
            test_finish = time.time()
            test_duration = (test_finish - test_start)
            test_finish_date = datetime.now()
            test_finsh_date_txt = test_finish_date.strftime("%A %B %d %H:%M:%S %Y")
            
            if key == " ":
                break
            elif test_duration > max_value:
                print("Current time " + "(" + str(test_duration) + ")" + " exceeds the maximum of " + str(max_value))
                break
       
        type_average_duration = type_sum_duration / number_of_types
        number_of_misses = number_of_types - number_of_hits
        
        if number_of_hits > 0:
            type_hit_average_duration = type_hit_sum_duration / number_of_hits
        else:
            type_hit_average_duration = "cannot be calculated."
        if number_of_misses > 0:
            type_miss_average_duration = type_miss_sum_duration / number_of_misses
        else:
            type_miss_average_duration = "cannot be calculated."
    
    print(Fore.BLUE + "Test finished!", Style.RESET_ALL)
    test_dict = {"Inputs": inputs_array, "Number of types": number_of_types, "Number of hits": number_of_hits,
            "Accuracy": accuracy_dict, "Test duration": test_duration, "Test start date": test_start_date_txt, 
            "Test finish date": test_finsh_date_txt, "Type average duration": type_average_duration,
            "Type hit average duration": type_hit_average_duration, "Type miss average duration": type_miss_average_duration}
    pprint(test_dict) 
            



#Modo de inputs máximo
def inputs_max_mode():
    print(Fore.RED + "PSR", Style.RESET_ALL + "typing test, Rafael & Nuno", today_date)
    print("Test running up to " + str(max_value) + " inputs.")
    print("Press any key to start the test")
    s_key = readkey()
        
    if s_key == s_key:
        test_start = time.time()
        test_start_date = datetime.now()
        test_start_date_txt = test_start_date.strftime("%A %B %d %H:%M:%S %Y")
        number_of_types = 0 
        number_of_hits = 0
        type_sum_duration = 0
        type_hit_sum_duration = 0
        type_miss_sum_duration = 0
    
        while True:
            random_letter = chr(random.randint(ord('a'), ord('z')))
            key_requested = time.time()
            print("Type letter " + Fore.BLUE + random_letter, Style.RESET_ALL)
            key = readkey()
            key_pressed = time.time()
            duration = (key_pressed - key_requested)
            type_sum_duration += duration
            
            if key == random_letter:
                type_hit_sum_duration += duration
                number_of_hits += 1
                print("You typed letter " + Fore.GREEN + key, Style.RESET_ALL)
            else:
                type_miss_sum_duration += duration
                print("You typed letter " + Fore.RED + key, Style.RESET_ALL)
           
            inputs_add = inputs(random_letter, key, duration)
            inputs_array.append(inputs_add)
            number_of_types +=1
            accuracy = ((number_of_hits / number_of_types) * 100)
            accuracy_dict = str(accuracy) + "%"
            test_finish = time.time()
            test_duration = (test_finish - test_start)
            test_finish_date = datetime.now()
            test_finsh_date_txt = test_finish_date.strftime("%A %B %d %H:%M:%S %Y")
            
            if key == " ":
                break
            elif number_of_types == max_value:
                print("Current number of inputs " + "(" + str(number_of_types) + ")" + " reaches maximum of " + str(max_value))
                break
       
        type_average_duration = type_sum_duration / number_of_types
        number_of_misses = number_of_types - number_of_hits
        
        if number_of_hits > 0:
            type_hit_average_duration = type_hit_sum_duration / number_of_hits
        else:
            type_hit_average_duration = "cannot be calculated."
        if number_of_misses > 0:
            type_miss_average_duration = type_miss_sum_duration / number_of_misses
        else:
            type_miss_average_duration = "cannot be calculated."
    
    print(Fore.BLUE + "Test finished!", Style.RESET_ALL)
    test_dict = {"Inputs": inputs_array, "Number of types": number_of_types, "Number of hits": number_of_hits,
            "Accuracy": accuracy_dict, "Test duration": test_duration, "Test start date": test_start_date_txt, 
            "Test finish date": test_finsh_date_txt, "Type average duration": type_average_duration,
            "Type hit average duration": type_hit_average_duration, "Type miss average duration": type_miss_average_duration}
    pprint(test_dict) 
    
    

def main():
    if args.use_time_mode == True and max_value != None:
        time_max_mode()
    elif args.use_time_mode == False and max_value != None:
        inputs_max_mode()
    else:
        print("Define your arguments or type -h for help")

        
if __name__ == "__main__":
    main()
