#!/usr/bin/env python3
from email.mime import image
import cv2
import numpy as np

def main():

    image_filename = "/home/nunoc99/Desktop/MEAI/psr_22-23/Parte05/images/atlas2000_e_atlasmv.png"

    image_rgb = cv2.imread(image_filename, cv2.IMREAD_COLOR) # Load an image

    lower_bound = np.array([0, 60, 0])
    upper_bound = np.array([50,256,50])
    #masking the image using inRange() function
    imagemask = cv2.inRange(image_rgb, lower_bound, upper_bound)

    cv2.imshow('RGB Image', image_rgb)
    cv2.imshow('Image Mask', imagemask)
    
    cv2.waitKey(0) # wait for a key press before proceeding

if __name__ == "__main__":
    main()