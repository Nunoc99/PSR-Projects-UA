#!/usr/bin/env python3
import cv2
import argparse

def main():

    image_filename = "/home/nunoc99/Desktop/MEAI/psr_22-23/Parte05/images/atlascar2.png"
    image_rgb = cv2.imread(image_filename, cv2.IMREAD_COLOR) # Load an image
    image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)
    retval, image_thresholded = cv2.threshold(image_gray, 128, 255, cv2.THRESH_BINARY)
    cv2.imshow('RGB Image', image_rgb)  # Display the image
    cv2.imshow('GRAY Image', image_gray)  # Display the image
    cv2.imshow('Thresholded Image', image_thresholded)  # Display the image
    cv2.waitKey(0) # wait for a key press before proceeding

if __name__ == "__main__":
    main()