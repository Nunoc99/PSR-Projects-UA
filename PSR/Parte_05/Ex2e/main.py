#!/usr/bin/env python3
from email.mime import image
import cv2
import numpy as np

def main():

    image_filename = "/home/nunoc99/Desktop/MEAI/psr_22-23/Parte05/images/atlas2000_e_atlasmv.png"

    image_rgb = cv2.imread(image_filename, cv2.IMREAD_COLOR) # Load an image

    image_hsv = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2HSV)
    lower_black = np.array([60, 25, 25])
    upper_black = np.array([86,255,255])

    imagemask = cv2.inRange(image_hsv, lower_black, upper_black)

    cv2.imshow('RGB Image', image_rgb)
    cv2.imshow('Image Mask', imagemask)
    
    cv2.waitKey(0) # wait for a key press before proceeding

if __name__ == "__main__":
    main()