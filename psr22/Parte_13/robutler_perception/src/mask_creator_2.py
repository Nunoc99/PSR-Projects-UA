#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2
import numpy as np
from copy import deepcopy
import array
import json
from pprint import pprint

window_name = "Original"
window_name2 = "Segmented"

def detectcolor():
    pass

def trackbars(x):
    print(x)


def msgReceivedCallback(msg):
    rospy.loginfo("I received an image")

        
    lvl1 = cv2.getTrackbarPos("Max B", window_name2)
    lvl2 = cv2.getTrackbarPos("Min B", window_name2)
    lvl3 = cv2.getTrackbarPos("Max G", window_name2)
    lvl4 = cv2.getTrackbarPos("Min G", window_name2)
    lvl5 = cv2.getTrackbarPos("Max R", window_name2)
    lvl6 = cv2.getTrackbarPos("Min R", window_name2)

    limit_dict ={'limits_dict': {'B': {'max': lvl1, 'min': lvl2},
        'G': {'max': lvl3, 'min': lvl4},
        'R': {'max': lvl5, 'min': lvl6}}}
    limit_dicts = limit_dict['limits_dict']
    lvlmax = np.array([limit_dicts['B']['max'], limit_dicts['G']['max'], limit_dicts['R']['max']])
    lvlmin = np.array([limit_dicts['B']['min'], limit_dicts['G']['min'], limit_dicts['R']['min']])

    bridge = CvBridge()

    cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
    cv2.imshow(window_name, cv_image)

    mask_frame = cv2.inRange(cv_image, lvlmin, lvlmax)
    flip_video2 = cv2.flip(mask_frame, 1)
    cv2.imshow(window_name2, flip_video2)

    pressed_key = cv2.waitKey(1)
    
def main():

    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(window_name2, cv2.WINDOW_AUTOSIZE)

    cv2.createTrackbar("Max B", window_name2, 0, 255, trackbars)
    cv2.createTrackbar("Min B", window_name2, 0, 255, trackbars)
    cv2.createTrackbar("Max G", window_name2, 0, 255, trackbars)
    cv2.createTrackbar("Min G", window_name2, 0, 255, trackbars)
    cv2.createTrackbar("Max R", window_name2, 0, 255, trackbars)
    cv2.createTrackbar("Min R", window_name2, 0, 255, trackbars)


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

if __name__ == '__main__':
    main()