#!/usr/bin/env python3
import cv2

def main():
    image_filename = "/home/nunoc99/Desktop/MEAI/psr_22-23/Parte05/images/atlascar.png"
    image_rgb = cv2.imread(image_filename, cv2.IMREAD_COLOR) # Load an image

    center_coordinates = (300, 200)
    radius = 20
    color = (0, 255, 0) #color in BGR
    thickness = 2

    image_rgb = cv2.circle(image_rgb, center_coordinates, radius, color, thickness) # cv2 circle method

    cv2.imshow('RGB Image', image_rgb)  # Display the image
    cv2.waitKey(0) # wait for a key press before proceeding

if __name__ == "__main__":
    main()