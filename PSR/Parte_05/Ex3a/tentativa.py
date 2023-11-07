#!/usr/bin/env python3
import cv2

def onTrackbar(x):
    pass

def main():

    cv2.namedWindow('Color Track Bar')
    hh = 'Max'
    h1 = 'Min'

    wnd = 'Colobars'

    cv2.createTrackbar("Max", "Color Track Bar", 0, 255, onTrackbar)
    cv2.createTrackbar("Min", "Color Track Bar", 0, 255, onTrackbar)

    img = cv2.imread('/home/nunoc99/Desktop/MEAI/psr_22-23/Parte05/images/atlascar.png')
    
    while True:
        hul = cv2.getTrackbarPos("Max", "Color Track Bar")
        huh = cv2.getTrackbarPos("Min", "Color Track Bar")

        retval, thresh1 = cv2.threshold(img, hul, huh, cv2.THRESH_BINARY)
        # retval, thresh2 = cv2.threshold(img, hul, huh, cv2.THRESH_TOZERO)

        cv2.imshow("thresh1", thresh1)
        # cv2.imshow("thresh2", thresh2)

        if cv2.waitKey(0):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()