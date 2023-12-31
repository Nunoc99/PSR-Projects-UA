#!/usr/bin/env python3

import cv2
import argparse 
import json
import numpy as np
from colorama import Fore, Style
from copy import deepcopy
from datetime import date, datetime
import copy

#Definição de Argumentos/help menu
parser = argparse.ArgumentParser(description="Definition of test mode:")

parser.add_argument('-j','--json',help='Full path to json file.',required=True, type=argparse.FileType('r'))
parser.add_argument("-usp", "--use_shake_prevention", help="Shake prevention.", action="store_true", default=False)
parser.add_argument("-uvs", "--use_video_stream", help="Use video stream as canvas.", action="store_true", default=False)
parser.add_argument("-np", "--numbered_paint", help="Paint a numbered image.", action="store_true", default=False)                        
args = parser.parse_args()

# use_shake_prevention = args.use_shake_prevention
# use_video_stream = args.use_video_stream

def selectbiggestComponents(image):
    connectivity=8
    nLabels, output, stats, centroids = cv2.connectedComponentsWithStats(image, connectivity,cv2.CV_32S)
    sizes = stats[1:, -1]
    nLabels = nLabels - 1
    x = None
    y = None
    final_image = np.zeros(output.shape, dtype=np.uint8)
    largest_component=0

    for k in range(0, nLabels):
        if sizes[k] >= largest_component:
        
            largest_component = sizes[k]
            x, y = centroids[k + 1]
            final_image[output == k + 1] = 255

    return (final_image, x, y)

def distanceCalculate(p1, p2):
    """p1 and p2 in format (x1,y1) and (x2,y2) tuples"""
    dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    return round(dis)


#Function to mix the captured image with drawing (for uvs mode)
def mix_images(canvas, frame):
    lvlmax_white = np.array([255, 255, 255])
    lvlmin_white = np.array([255, 255, 255])
    mask_for_whites = cv2.inRange(canvas, lvlmin_white, lvlmax_white) # Defining a mask for white pixels
    mask_for_whites_bool=mask_for_whites.astype(np.bool)
    result = copy.deepcopy(frame)
    result[~mask_for_whites_bool] = canvas[~mask_for_whites_bool] # Blending the non white pixels of canvas with captured image

    return result



def normal_mode():

    print("\nNormal mode in execution...")
    print("-----------------Key Commands Menu---------------------\n")
    print("Press 'r' to change the pencil color to" + Fore.RED + " red.\n" + Style.RESET_ALL)
    print("Press 'g' to change the pencil color to" + Fore.GREEN + " green.\n" + Style.RESET_ALL)
    print("Press 'b' to change the pencil color to" + Fore.BLUE + " blue.\n" + Style.RESET_ALL)
    print("Press 'y' to change the pencil color to" + Fore.YELLOW + " yellow.\n" + Style.RESET_ALL)
    print("Press '+' to increase the pencil line thickness.\n")
    print("Press '-' to decrease the pencil line thickness.\n")
    print("Press 'c' to clean the canvas.\n")
    print("Press 'w' to save the drawing/painting.\n")
    print("------------------------------------------------------\n")

    with args.json as file:
        limits=json.load(file)
        # print(limits)
    limits_dict=limits['limits_dict']
    
    lvlmax = np.array([limits_dict['B']['max'], limits_dict['G']['max'], limits_dict['R']['max']])
    lvlmin = np.array([limits_dict['B']['min'], limits_dict['G']['min'], limits_dict['R']['min']])

    vid = cv2.VideoCapture(0)
    retval, frame = vid.read()
    window_name = "Orignal"
    window_name2 = "Segmented"
    window_name3 = "Mask Largest component"
    window_name4 = "Canvas"
    blank_image = np.ones(frame.shape, dtype = np.uint8)
    blank_image = 255* blank_image
    #blank_image = cv2.imread("white_image.png", cv2.IMREAD_COLOR)
    thickness=3
    clr=(0,255,255)
    centroides=[]

    #For shapes
    drawing_circle = False
    drawing_rectangle = False


    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.namedWindow(window_name2, cv2.WINDOW_NORMAL)
    cv2.namedWindow(window_name3, cv2.WINDOW_NORMAL)
    cv2.namedWindow(window_name4, cv2.WINDOW_NORMAL)

    while True:

        retval, frame = vid.read() 

        # blank_image = np.ones((original_dimensions[0], original_dimensions[1], 3), dtype = np.uint8)
        # blank_image = 255* blank_image
        # flip_video = cv2.flip(frame, 1)
        

        #display masked resulting frame
        mask_frame = cv2.inRange(frame, lvlmin, lvlmax)
        flip_video2 = cv2.flip(mask_frame, 1)
        cv2.imshow(window_name2, flip_video2)

        #mask largest component result frame
        mask_largest = selectbiggestComponents(mask_frame)
        flip_video3 = cv2.flip(mask_largest[0], 1)
        cv2.imshow(window_name3, flip_video3)
        x=mask_largest[1]
        y=mask_largest[2]
        centroide=(int(x),int(y)) 
        centroides.append(centroide)
        k=centroides.index(centroide)
        start_point=centroides[k-1]
        end_point=centroides[k]


        #painting de mask largest component on original image
        frame_copy=np.copy(frame)
        frame_copy[mask_largest[0]==255]=(0,255,0)
        
        #adição da cruz na imagem original
        cv2.line(frame_copy, (int(x) - 5,int(y)), (int(x) + 5, int(y)), (0, 0, 255), 3)
        cv2.line(frame_copy, (int(x), int(y) + 5), (int(x), int(y) - 5), (0, 0, 255), 3)

        flip_video4 = cv2.flip(frame_copy, 1)
        cv2.imshow(window_name, flip_video4)


        #desenhar na tela branca.
        if not drawing_rectangle and not drawing_circle:

            cv2.line(blank_image, start_point, end_point, clr, thickness)
            flip_video5=cv2.flip(blank_image, 1)
            cv2.imshow(window_name4, flip_video5)

        

        pressed_key = cv2.waitKey(1)

        if pressed_key == ord('q'):
            break
        elif pressed_key == ord('w'): # save drawing
            current_data = datetime.now().strftime("%H:%M:%S_%Y")
            
            todays_date=date.today()
            dia=todays_date.day #retira o valor do dia em str
            month=todays_date.month #retira o valor do mes em str
            month_object = datetime.strptime(str(month), "%m") # converte a str para time em 01,02,03
            day_object= datetime.strptime(str(dia), "%d") # converte a str para time em 01,02,03
            month_name = month_object.strftime("%b") #converte o 01,02 para mes em out set...
            day_name=day_object.strftime('%a') #converte o 01,02 para dia em seg, ter, qua...
            cv2.imwrite('drawing_'+day_name +'_'+month_name+  '_' + str(dia)+'_' + current_data + '.png', flip_video5)
            print('drawing saved in document: '+'drawing_'+day_name +'_'+month_name+  '_' + str(dia)+'_' + current_data + '.png')

        elif pressed_key == ord('c'): # clean the canvas
            centroides=[] #reset no centroides usados para desenhar os traços
            blank_image.fill(255) #reset na imagem com tudo para branco.
            print("The canvas is clean.")
            pass

        elif pressed_key == ord('r'): # change color to red
            clr = (0,0,255)
            print("Color changed to " + Fore.RED + "RED" + Style.RESET_ALL)

        elif pressed_key == ord('g'): # change color to green
            clr = (0,255,0)
            print("Color changed to " + Fore.GREEN + "GREEN" + Style.RESET_ALL)

        elif pressed_key == ord('b'): # change color to blue
            clr = (255,0,0)
            print("Color changed to " + Fore.BLUE + "BLUE" + Style.RESET_ALL)

        elif pressed_key == ord('+'): # increase pencil line size
            thickness +=1
            print('thickness is ' + str(thickness))

        elif pressed_key == ord('-'): # decrease pencil line sizw
            
            if thickness==1:
                print('thickness can not be 0 or less.')
                print('thickness is ' + str(thickness))
            else:
                thickness -=1
                print('thickness is ' + str(thickness))


        #Draw a rectangle
        elif pressed_key == ord('s'):
            if not drawing_rectangle:
                first_point = centroide
                print('You started drawing a rectangle.')
                drawing_rectangle = True
            elif drawing_rectangle:
                cv2.rectangle(blank_image, first_point, centroide, clr, thickness)
                print('You just finished a rectangle.')
                drawing_rectangle = False

        #Draw a circle
        elif pressed_key == ord('e'):
            if not drawing_circle:
                center = centroide
                print('You started drawing a circle.')
                drawing_circle = True
            elif drawing_circle:
                cv2.circle(blank_image, center, circle_radius, clr, thickness)
                print('You just finished a circle.')
                drawing_circle = False

        # If the drawing flags are activated, it is shown the result in real time

        elif drawing_rectangle:
            image_rectangle = np.copy(blank_image)
            cv2.rectangle(image_rectangle, first_point, centroide, clr, thickness)
            flip_video5=cv2.flip(image_rectangle, 1)
            cv2.imshow(window_name4, flip_video5)


        elif drawing_circle:
            circle_radius = distanceCalculate(center,centroide)
            image_circle = np.copy(blank_image)
            cv2.circle(image_circle, center, circle_radius, clr, thickness)
            flip_video5=cv2.flip(image_circle, 1)
            cv2.imshow(window_name4, flip_video5)


    vid.release()
    cv2.destroyAllWindows()

def usp_mode():
    print("\nUse shake prevention mode in execution...\n")
    print("-----------------Key Commands Menu---------------------\n")
    print("Press 'r' to change the pencil color to" + Fore.RED + " red.\n" + Style.RESET_ALL)
    print("Press 'g' to change the pencil color to" + Fore.GREEN + " green.\n" + Style.RESET_ALL)
    print("Press 'b' to change the pencil color to" + Fore.BLUE + " blue.\n" + Style.RESET_ALL)
    print("Press '+' to increase the pencil line thickness.\n")
    print("Press '-' to decrease the pencil line thickness.\n")
    print("Press 'c' to clean the canvas.\n")
    print("Press 'w' to save the drawing/painting.\n")
    print("------------------------------------------------------\n")





def uvs_mode():
    print("\nUse video stream drawing mode in execution...\n")
    print("-----------------Key Commands Menu---------------------\n")
    print("Press 'r' to change the pencil color to" + Fore.RED + " red.\n" + Style.RESET_ALL)
    print("Press 'g' to change the pencil color to" + Fore.GREEN + " green.\n" + Style.RESET_ALL)
    print("Press 'b' to change the pencil color to" + Fore.BLUE + " blue.\n" + Style.RESET_ALL)
    print("Press '+' to increase the pencil line thickness.\n")
    print("Press '-' to decrease the pencil line thickness.\n")
    print("Press 'c' to clean the canvas.\n")
    print("Press 'w' to save the drawing/painting.\n")
    print("------------------------------------------------------\n")

    with args.json as file:
        limits=json.load(file)
        # print(limits)
    limits_dict=limits['limits_dict']
    
    lvlmax = np.array([limits_dict['B']['max'], limits_dict['G']['max'], limits_dict['R']['max']])
    lvlmin = np.array([limits_dict['B']['min'], limits_dict['G']['min'], limits_dict['R']['min']])

    vid = cv2.VideoCapture(0)
    retval, frame = vid.read()
    window_name = "Orignal"
    window_name2 = "Segmented"
    window_name3 = "Mask Largest component"
    window_name4 = "Canvas"
    blank_image = np.ones(frame.shape, dtype = np.uint8)
    blank_image = 255* blank_image
    thickness=3
    clr=(0,255,255)
    centroides=[]

    #For shapes
    drawing_circle = False
    drawing_rectangle = False


    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.namedWindow(window_name2, cv2.WINDOW_NORMAL)
    cv2.namedWindow(window_name3, cv2.WINDOW_NORMAL)
    cv2.namedWindow(window_name4, cv2.WINDOW_NORMAL)

    while True:

        retval, frame = vid.read() #capture for the original video

        frame_gui = copy.deepcopy(frame)
        flip_video = cv2.flip(frame_gui, 1)
        
        #display masked resulting frame
        mask_frame = cv2.inRange(frame, lvlmin, lvlmax)
        flip_video2 = cv2.flip(mask_frame, 1)
        cv2.imshow(window_name2, flip_video2)

        #mask largest component result frame
        mask_largest = selectbiggestComponents(mask_frame)
        flip_video3 = cv2.flip(mask_largest[0], 1)
        cv2.imshow(window_name3, flip_video3)
        x=mask_largest[1]
        y=mask_largest[2]
        centroide=(int(x),int(y)) 
        centroides.append(centroide)
        k=centroides.index(centroide)
        start_point=centroides[k-1]
        end_point=centroides[k]


        #painting de mask largest component on original image
        frame_copy=np.copy(frame)
        frame_copy[mask_largest[0]==255]=(0,255,0)
        
        #adição da cruz na imagem original
        cv2.line(frame_copy, (int(x) - 5,int(y)), (int(x) + 5, int(y)), (0, 0, 255), 3)
        cv2.line(frame_copy, (int(x), int(y) + 5), (int(x), int(y) - 5), (0, 0, 255), 3)

        flip_video4 = cv2.flip(frame_copy, 1)
        cv2.imshow(window_name, flip_video4)

        #STREAM CANVAS DRAWING

        if not drawing_rectangle and not drawing_circle:

            cv2.line(blank_image, start_point, end_point, clr, thickness)
            flip_video5=cv2.flip(blank_image, 1)
            cv2.imshow(window_name4, mix_images(flip_video5, flip_video))

        pressed_key = cv2.waitKey(1)

        if pressed_key == ord('q'):
            break
        elif pressed_key == ord('w'): # save drawing
            current_data = datetime.now().strftime("%H:%M:%S_%Y")
            
            todays_date=date.today()
            dia=todays_date.day #retira o valor do dia em str
            month=todays_date.month #retira o valor do mes em str
            month_object = datetime.strptime(str(month), "%m") # converte a str para time em 01,02,03
            day_object= datetime.strptime(str(dia), "%d") # converte a str para time em 01,02,03
            month_name = month_object.strftime("%b") #converte o 01,02 para mes em out set...
            day_name=day_object.strftime('%a') #converte o 01,02 para dia em seg, ter, qua...
            cv2.imwrite('drawing_'+day_name +'_'+month_name+  '_' + str(dia)+'_' + current_data + '.png', flip_video5)
            print('drawing saved in document: '+'drawing_'+day_name +'_'+month_name+  '_' + str(dia)+'_' + current_data + '.png')

        elif pressed_key == ord('c'): # clean the canvas
            centroides=[] #reset no centroides usados para desenhar os traços
            blank_image.fill(255) #reset na imagem com tudo para branco.
            print("The canvas is clean.")
            pass

        elif pressed_key == ord('r'): # change color to red
            clr = (0,0,255)
            print("Color changed to " + Fore.RED + "RED" + Style.RESET_ALL)

        elif pressed_key == ord('g'): # change color to green
            clr = (0,255,0)
            print("Color changed to " + Fore.GREEN + "GREEN" + Style.RESET_ALL)

        elif pressed_key == ord('b'): # change color to blue
            clr = (255,0,0)
            print("Color changed to " + Fore.BLUE + "BLUE" + Style.RESET_ALL)

        elif pressed_key == ord('+'): # increase pencil line size
            thickness +=1
            print('thickness is ' + str(thickness))

        elif pressed_key == ord('-'): # decrease pencil line sizw
            
            if thickness==1:
                print('thickness can not be 0 or less.')
                print('thickness is ' + str(thickness))
            else:
                thickness -=1
                print('thickness is ' + str(thickness))

        #Draw a rectangle
        elif pressed_key == ord('s'):
            if not drawing_rectangle:
                first_point = centroide
                print('You started drawing a rectangle.')
                drawing_rectangle = True
               
            elif drawing_rectangle:
                cv2.rectangle(blank_image, first_point, centroide, clr, thickness)
                print('You just finished a rectangle.')
                drawing_rectangle = False
                

        #Draw a circle
        elif pressed_key == ord('e'):
            if not drawing_circle:
                center = centroide
                print('You started drawing a circle.')
                drawing_circle = True
            elif drawing_circle:
                cv2.circle(blank_image, center, circle_radius, clr, thickness)
                print('You just finished a circle.')
                drawing_circle = False

        # If the drawing flags are activated, it is shown the result in real time

        elif drawing_rectangle:
            image_rectangle = np.copy(blank_image)
            cv2.rectangle(image_rectangle, first_point, centroide, clr, thickness)
            flip_video5=cv2.flip(image_rectangle, 1)
            cv2.imshow(window_name4, mix_images(flip_video5, flip_video))


        elif drawing_circle:
            circle_radius = distanceCalculate(center,centroide)
            image_circle = np.copy(blank_image)
            cv2.circle(image_circle, center, circle_radius, clr, thickness)
            flip_video5=cv2.flip(image_circle, 1)
            cv2.imshow(window_name4, mix_images(flip_video5, flip_video))
                

    vid.release()
    cv2.destroyAllWindows()



def numbered_paint():

    print("\nNumbered paint mode in execution...\n")
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

    with args.json as file:
        limits=json.load(file)
        # print(limits)
    limits_dict=limits['limits_dict']
    
    lvlmax = np.array([limits_dict['B']['max'], limits_dict['G']['max'], limits_dict['R']['max']])
    lvlmin = np.array([limits_dict['B']['min'], limits_dict['G']['min'], limits_dict['R']['min']])

    vid = cv2.VideoCapture(0)
    retval, frame = vid.read()
    window_name = "Orignal"
    window_name2 = "Segmented"
    window_name3 = "Mask Largest component"
    window_name4 = "Canvas"
    numbered_image = cv2.imread("/home/nunoc99/Desktop/MEAI/PSR/Parte_07/pinguim.png")
    numbered_image_copy = np.copy(numbered_image)
    thickness=3
    clr=(0,255,255)
    centroides=[]


    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.namedWindow(window_name2, cv2.WINDOW_NORMAL)
    cv2.namedWindow(window_name3, cv2.WINDOW_NORMAL)
    cv2.namedWindow(window_name4, cv2.WINDOW_NORMAL)

    while True:

        retval, frame = vid.read() 

        # blank_image = np.ones((original_dimensions[0], original_dimensions[1], 3), dtype = np.uint8)
        # blank_image = 255* blank_image
        # flip_video = cv2.flip(frame, 1)
        

        #display masked resulting frame
        mask_frame = cv2.inRange(frame, lvlmin, lvlmax)
        flip_video2 = cv2.flip(mask_frame, 1)
        cv2.imshow(window_name2, flip_video2)

        #mask largest component result frame
        mask_largest = selectbiggestComponents(mask_frame)
        flip_video3 = cv2.flip(mask_largest[0], 1)
        cv2.imshow(window_name3, flip_video3)
        x=mask_largest[1]
        y=mask_largest[2]
        centroide=(int(x),int(y)) 
        centroides.append(centroide)
        k=centroides.index(centroide)
        start_point=centroides[k-1]
        end_point=centroides[k]


        #painting de mask largest component on original image
        frame_copy=np.copy(frame)
        frame_copy[mask_largest[0]==255]=(0,255,0)
        
        #adição da cruz na imagem original
        cv2.line(frame_copy, (int(x) - 5,int(y)), (int(x) + 5, int(y)), (0, 0, 255), 3)
        cv2.line(frame_copy, (int(x), int(y) + 5), (int(x), int(y) - 5), (0, 0, 255), 3)

        flip_video4 = cv2.flip(frame_copy, 1)
        cv2.imshow(window_name, flip_video4)

        #painting on the numbered image
        cv2.line(numbered_image_copy, start_point, end_point, clr, thickness)
        cv2.imshow(window_name4, numbered_image_copy)
        

        pressed_key = cv2.waitKey(1)

        if pressed_key == ord('q'):
            break
        elif pressed_key == ord('w'): # save drawing
            current_data = datetime.now().strftime("%H:%M:%S_%Y")
            
            todays_date=date.today()
            dia=todays_date.day #retira o valor do dia em str
            month=todays_date.month #retira o valor do mes em str
            month_object = datetime.strptime(str(month), "%m") # converte a str para time em 01,02,03
            day_object= datetime.strptime(str(dia), "%d") # converte a str para time em 01,02,03
            month_name = month_object.strftime("%b") #converte o 01,02 para mes em out set...
            day_name=day_object.strftime('%a') #converte o 01,02 para dia em seg, ter, qua...
            cv2.imwrite('drawing_'+day_name +'_'+month_name+  '_' + str(dia)+'_' + current_data + '.png', numbered_image_copy)
            print('drawing saved in document: '+'drawing_'+day_name +'_'+month_name+  '_' + str(dia)+'_' + current_data + '.png')

        elif pressed_key == ord('c'): # clean the canvas
            centroides=[] #reset no centroides usados para desenhar os traços
            numbered_image_copy = numbered_image #reset na imagem com tudo para branco.
            print("The canvas is clean.")
            pass

        elif pressed_key == ord('r') or pressed_key == ord('1'): # change color to red
            clr = (0,0,255)
            print("Color changed to " + Fore.RED + "RED" + Style.RESET_ALL)

        elif pressed_key == ord('g') or pressed_key == ord('2'): # change color to green
            clr = (0,255,0)
            print("Color changed to " + Fore.GREEN + "GREEN" + Style.RESET_ALL)

        elif pressed_key == ord('b') or pressed_key == ord('3'): # change color to blue
            clr = (255,0,0)
            print("Color changed to " + Fore.BLUE + "BLUE" + Style.RESET_ALL)

        elif pressed_key == ord('y') or pressed_key == ord('4'): # change color to yellow
            clr = (0,255,255)
            print("Color changed to " + Fore.YELLOW + "YELLOW" + Style.RESET_ALL)

        elif pressed_key == ord('+'): # increase pencil line size
            thickness +=1
            print('thickness is ' + str(thickness))

        elif pressed_key == ord('-'): # decrease pencil line sizw
            
            if thickness==1:
                print('thickness can not be 0 or less.')
                print('thickness is ' + str(thickness))
            else:
                thickness -=1
                print('thickness is ' + str(thickness))


    vid.release()
    cv2.destroyAllWindows()


def main():

    if args.use_shake_prevention == True:
        usp_mode()
    elif args.use_video_stream == True:
        uvs_mode()
    elif args.numbered_paint == True:
        numbered_paint()
    else:
        normal_mode()

if __name__ == "__main__":
    main()