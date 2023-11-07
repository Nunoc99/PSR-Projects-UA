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
    imagemask = imagemask.astype(bool)

    b, g, r = cv2.split(image_rgb)
    b[imagemask] = 0
    g[imagemask] = 0
    r[imagemask] = 255
    image_rgb = cv2.merge((b, g, r))

    cv2.imshow('RGB Image', image_rgb)
    cv2.imshow('R channel', r)
    
    cv2.waitKey(0) # wait for a key press before proceeding

if __name__ == "__main__":
    main()