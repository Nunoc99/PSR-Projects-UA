#!/usr/bin/env python3
import cv2

def main():

    image_filename = "/home/nunoc99/Desktop/MEAI/psr_22-23/Parte05/images/atlascar2.png"

    image_rgb = cv2.imread(image_filename, cv2.IMREAD_COLOR) # Load an image
    thresholded_levelb = 50
    thresholded_levelg = 100
    thresholded_levelr = 150

    (B, G, R) = cv2.split(image_rgb)

    retval, image_thresholdedb = cv2.threshold(B, thresholded_levelb, 255, cv2.THRESH_BINARY)
    retval, image_thresholdedg = cv2.threshold(G, thresholded_levelg, 255, cv2.THRESH_BINARY)
    retval, image_thresholdedr = cv2.threshold(R, thresholded_levelr, 255, cv2.THRESH_BINARY)

    merged = cv2.merge([image_thresholdedb, image_thresholdedg, image_thresholdedr])

    cv2.imshow('Red', image_thresholdedr)  # Display the red in image
    cv2.imshow('Green', image_thresholdedg)  # Display the green in image
    cv2.imshow('Blue', image_thresholdedb)  # Display the blue in image
    cv2.imshow('Merged', merged)
    cv2.imshow('RGB Image', image_rgb)
    
    cv2.waitKey(0) # wait for a key press before proceeding

if __name__ == "__main__":
    main()