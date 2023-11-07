#!/usr/bin/env python3

import cv2
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


def main():

    # init of a ros node
    rospy.init_node('image_reader', anonymous=False)

    #create the publisher
    publisher = rospy.Publisher('~image', Image, queue_size=1)

    bridge = CvBridge()

    vid = cv2.VideoCapture(0)
    window_name = "image"
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():

        retval, frame = vid.read()
        flip_video = cv2.flip(frame, 1)
        
        cv2.imshow(window_name, flip_video)  # Display the image
        if cv2.waitKey(1) & 0xFF == ord('q'): # wait for a key press before proceeding
            break

        image_msg = bridge.cv2_to_imgmsg(flip_video, encoding="passthrough")

        publisher.publish(image_msg)
        rate.sleep()

    # vid.release()


if __name__ == "__main__":
    main()