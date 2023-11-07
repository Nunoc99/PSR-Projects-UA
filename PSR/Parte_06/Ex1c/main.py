#!/usr/bin/env python3
import cv2
import numpy as np
from copy import deepcopy

is_drawing = False
xs = []
ys = []

def printCoordinate(event, x, y, flags, params):
    print(x, ',',y)

    if event == cv2.EVENT_LBUTTONDOWN:
        if is_drawing:
            print("Stop drawing")
            is_drawing = False
        else:
            print("Start drawing")
            is_drawing = True
    
    elif event == cv2.EVENT_MOUSEMOVE:
        if is_drawing:
            xs.append(x)
            ys.append(y)

            for xi, yi in zip(xs, ys):
                cv2.line(gui_image, (xi, yi), (255,0,0), 2)

def main():

    global gui_image
    image_filename = "/home/nunoc99/Desktop/MEAI/PSR/Parte_06/Ex1c/White-400x600px2-600x400-21732.png"
    image_rgb = cv2.imread(image_filename, cv2.IMREAD_COLOR) # Load an image
    gui_image = deepcopy(image_rgb)
    cv2.namedWindow('RGB Image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('RGB Image', 600, 400)
    cv2.setMouseCallback('RGB Image', printCoordinate)

    while True:
        cv2.imshow('RGB Image', gui_image)  # Display the image
        cv2.waitKey(0) # wait for a key press before proceeding

if __name__ == "__main__":
    main()