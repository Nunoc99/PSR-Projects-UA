#!/usr/bin/env python3
import cv2


def main():
    capture = cv2.VideoCapture(0)

    window_name = "A5-Ex2"
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    retval, image = capture.read()
    cv2.imshow(window_name, image)  # Display the image
    
    cv2.waitKey(0) # wait for a key press before proceeding

if __name__ == "__main__":
    main()