#!/usr/bin/env python3
import cv2


def main():

    vid = cv2.VideoCapture(0)
    while True:

        window_name = "A5-Ex2"
        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

        retval, frame = vid.read()
        
        cv2.imshow(window_name, frame)  # Display the image

        if cv2.waitKey(1) & 0xFF == ord('q'): # wait for a key press before proceeding
            break

    vid.release()

if __name__ == "__main__":
    main()