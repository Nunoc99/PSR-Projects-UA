#!/usr/bin/env python3

import json
from colorama import Fore, Back
import numpy as np
import cv2
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

window_1 = "Subscriber"
window_2 = "Mask"

def TrackBars(x):
    pass

def msgReceivedCallback(msg):
    rospy.loginfo("I received an image")

    # Get ranges from trackbar and add to a dictionary
    b_min = cv2.getTrackbarPos('B min', window_2)
    b_max = cv2.getTrackbarPos('B max', window_2)
    g_min = cv2.getTrackbarPos('G min', window_2)
    g_max = cv2.getTrackbarPos('G max', window_2)
    r_min = cv2.getTrackbarPos('R min', window_2)
    r_max = cv2.getTrackbarPos('R max', window_2)

    limit = {'B': {'min': b_min, 'max': b_max},
             'G': {'min': g_min, 'max': g_max},
             'R': {'min': r_min, 'max': r_max}}

    # Convert the dict structure created before to numpy arrays, because is the structure that opencv uses it.
    min = np.array([limit['B']['min'], limit['G']['min'], limit['R']['min']])
    max = np.array([limit['B']['max'], limit['G']['max'], limit['R']['max']])

    bridge = CvBridge()

    cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
    cv2.imshow(window_1, cv_image)

    # Create mask using cv2.inRange. The output is still in uint8
    mask_frame = cv2.inRange(cv_image, min, max)

    # Show segmented image
    cv2.imshow(window_2, mask_frame)  # Display the image

    key = cv2.waitKey(1)  # Wait a key to stop the program

    # Keyboard inputs to finish
    if key == ord('q'):
        print(Fore.RED + '"q" (quit) pressed, exiting the program without saving' + Fore.RESET)
        cv2.destroyAllWindows()
    elif key == ord('w'):
        print(Fore.GREEN + '"w" (write) pressed, exiting the program and saving' + Fore.RESET)
        file_name = 'limits.json'
        with open(file_name, 'w') as file_handle:
            print("Creating file with threshold limits" + file_name)
            json.dump(limit, file_handle)
            cv2.destroyAllWindows()

def main():

    cv2.namedWindow(window_1, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(window_2, cv2.WINDOW_AUTOSIZE)

    # Create trackbars to control the threshold to binarize
    cv2.createTrackbar('B min', window_2, 0, 255, TrackBars)
    cv2.createTrackbar('B max', window_2, 0, 255, TrackBars)
    cv2.createTrackbar('G min', window_2, 0, 255, TrackBars)
    cv2.createTrackbar('G max', window_2, 0, 255, TrackBars)
    cv2.createTrackbar('R min', window_2, 0, 255, TrackBars)
    cv2.createTrackbar('R max', window_2, 0, 255, TrackBars)
    # Set the trackbars positions to 255 for maximum trackbars
    cv2.setTrackbarPos('B max', window_2, 255)
    cv2.setTrackbarPos('G max', window_2, 255)
    cv2.setTrackbarPos('R max', window_2, 255)

    # Hotkeys
    print('\nUse the trackbars to define the threshold limits as you wish.')
    print(Back.GREEN + '\nStart getting sensor image.' + Back.RESET)
    print(Fore.GREEN + '\nPress "w" to exit and save the threshold' + Fore.RESET)
    print(Fore.RED + 'Press "q" to exit without saving the threshold' + Fore.RESET)
    
    # Initialization of a ros node
    rospy.init_node('camera_subscriber', anonymous=True)

    # Init the subscriber
    rospy.Subscriber('/camera/rgb/image_raw', Image, msgReceivedCallback)
    
    # ------------------------------------
    # Execution 
    # ------------------------------------
    rospy.spin()

    # ------------------------------------
    # Termination 
    # ------------------------------------

if __name__ == "__main__":
    main()
