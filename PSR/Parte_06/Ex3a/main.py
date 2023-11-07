#!/usr/bin/env python3
import cv2
import sys


def main():
    #cascPath = sys.argv[1]
    haar_file = 'data/haarcascade/haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(haar_file)
    vid = cv2.VideoCapture(0)

    while True:

        window_name = "A5-Ex2"
        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

        retval, frame = vid.read()
        image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detecting faces

        scaleFactor = 1.2
        minNeighbors = 5
        minSize = (40, 40)
        flags = cv2.CV_HAAR_SCALE_IMAGE
  
        faces = faceCascade.detectMultiScale(image_gray, scaleFactor, minNeighbors, minSize, flags)
        
        #detect rectangle

        for (x, y, w, h) in faces:
            start_point = (x, y)
            end_point = (x+w, y+h)
            color = (0, 255, 0)
            thickness = 2
            cv2.rectangle(frame, start_point, end_point, color, thickness)

        cv2.imshow(window_name, frame)  # Display the image

        if cv2.waitKey(1) & 0xFF == ord('q'): # wait for a key press before proceeding
            break

    vid.release()

if __name__ == "__main__":
    main()