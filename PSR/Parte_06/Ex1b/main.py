#!/usr/bin/env python3
import cv2

def main():
    image_filename = "/home/nunoc99/Desktop/MEAI/psr_22-23/Parte05/images/atlascar.png"
    image_rgb = cv2.imread(image_filename, cv2.IMREAD_COLOR) # Load an image

    org = (50, 50)
    font = cv2.FONT_HERSHEY_PLAIN
    fontScale = 1
    color = (0, 0, 255) #color BGR
    thickness = 2

    image_rgb = cv2.putText(image_rgb, 'PSR', org, font, fontScale, color, thickness, cv2.LINE_AA)

    cv2.imshow('RGB Image', image_rgb)  # Display the image
    cv2.waitKey(0) # wait for a key press before proceeding

if __name__ == "__main__":
    main()