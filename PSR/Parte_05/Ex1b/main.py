#!/usr/bin/env python3

import cv2
import argparse


def main():

    parser=argparse.ArgumentParser(description = "Path to image")
    parser.add_argument("-img", "--image_path", help = "Mode: Time", default = "/home/nunoc99/Desktop/MEAI/psr_22-23/Parte05/images/atlascar.png")
    parser.add_argument("-img2", "--image_path2", help = "Mode: Time", default = "/home/nunoc99/Desktop/MEAI/psr_22-23/Parte05/images/atlascar2.png")
    args = parser.parse_args()

    print(args.image_path)
    print(args.image_path2)

    image_filename = args.image_path
    image = cv2.imread(image_filename, cv2.IMREAD_COLOR) # Load an image
    cv2.imshow('window', image)  # Display the image
    cv2.waitKey(0) # wait for a key press before proceeding

    image_filename = args.image_path2
    image = cv2.imread(image_filename, cv2.IMREAD_COLOR) # Load an image
    cv2.imshow('window', image)  # Display the image
    cv2.waitKey(0) # wait for a key press before proceeding

    exit(0)

if __name__ == "__main__":
    main()