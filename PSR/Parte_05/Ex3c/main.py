#!/usr/bin/env python3
import cv2
import argparse

def onTrackbar(x):
    pass

def main():

    cv2.namedWindow('window - Ex3a')
    hh = 'Max'
    h1 = 'Min'

    wnd = 'Colobars'

    cv2.createTrackbar("Max", "window - Ex3a", 0, 255, onTrackbar)
    cv2.createTrackbar("Min", "window - Ex3a", 0, 255, onTrackbar)

    cv2.setMouseCallback("window - Ex3a", onMouse, userdata)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-img", "--image_path", help = "Mode: Time", default = "/home/nunoc99/Desktop/MEAI/psr_22-23/Parte05/images/atlascar.png")
    args = parser.parse_args()

    image_filename = args.image_path
    img = cv2.imread(image_filename, cv2.IMREAD_COLOR)  # Load an image

    while True:
        lvl1 = cv2.getTrackbarPos("Max", "window - Ex3a")
        lvl2 = cv2.getTrackbarPos("Min", "window - Ex3a")

        retval, thresh1 = cv2.threshold(img, lvl1, lvl2, cv2.THRESH_BINARY) 
        
        cv2.imshow("Thresholded Image", thresh1)

        if cv2.waitKey(1) == 27: # 27 caracter of escape
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()