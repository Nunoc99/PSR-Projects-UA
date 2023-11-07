#!/usr/bin/env python3

import rospy
from colorama import Fore, Back
from std_msgs.msg import String, Bool
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2
import numpy as np
import imutils
from datetime import datetime

sphere_v_lvlmax = np.array([255, 0, 210])
sphere_v_lvlmin = np.array([90, 0, 55])

lvlmin = np.array([50, 50, 50])
lvlmax = np.array([50, 50, 50])

mask_tolerance = 50

window_name = "Original"
window_name2 = "Adapted Mask"
window_name3 = "Violet Sphere Mask"
window_name4 = "People Detection"

threshold_whites = 500

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()



def mouse(event,x,y,flags,param):
    global colorsB, colorsG, colorsR, lvlmax, lvlmin

    if event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition
        colorsB = cv_image[y,x,0]
        colorsG = cv_image[y,x,1]
        colorsR = cv_image[y,x,2]
        colors = cv_image[y,x]
        print("Red: ",colorsR)
        print("Green: ",colorsG)
        print("Blue: ",colorsB)
        print("BRG Format: ",colors)
        print("Coordinates of pixel: X: ",x,"Y: ",y)
        lvlmax = np.array([int(colorsB) + mask_tolerance, int(colorsG) + mask_tolerance, int(colorsR) + mask_tolerance])
        lvlmin = np.array([int(colorsB) - mask_tolerance, int(colorsG) - mask_tolerance, int(colorsR) - mask_tolerance])
        limit_dict ={'limits_dict': {'B': {'max': int(lvlmax[0]), 'min': int(lvlmin[0])},
            'G': {'max': int(lvlmax[1]), 'min': int(lvlmin[1])},
            'R': {'max': int(lvlmax[2]), 'min': int(lvlmin[2])}}}

    if event == cv2.EVENT_RBUTTONDOWN: #checks mouse right button down condition
        now = datetime.now()
        date_time = now.strftime("%m%d%Y%H%M%S")
        filename = 'robutler_screenshot' + date_time + '.png'
        cv2.imwrite(filename, cv_image)
        print("Saving screenshot locally")
 


def selectbiggestComponents(image):
    connectivity=8
    nLabels, output, stats, centroids = cv2.connectedComponentsWithStats(image, connectivity,cv2.CV_32S)
    sizes = stats[1:, -1]
    nLabels = nLabels - 1
    x = None
    y = None
    final_image = np.zeros(output.shape, dtype=np.uint8)
    largest_component=0

    for k in range(0, nLabels):
        if sizes[k] >= largest_component:
        
            largest_component = sizes[k]
            x, y = centroids[k + 1]
            final_image[output == k + 1] = 255

    return (final_image, x, y)

def msgReceivedCallback(msg):

    global cv_image

    # rospy.loginfo("I received an image")

    bridge = CvBridge()

    cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
    cv2.imshow(window_name, cv_image)

    mask_frame_adapt = cv2.inRange(cv_image, lvlmin, lvlmax)

    mask_frame_spherev = cv2.inRange(cv_image, sphere_v_lvlmin, sphere_v_lvlmax)

    mask_largest_adapt = selectbiggestComponents(mask_frame_adapt)

    mask_largest_spherev = selectbiggestComponents(mask_frame_spherev)

    
    cv2.imshow(window_name2, mask_largest_adapt[0])

    cv2.imshow(window_name3, mask_largest_spherev[0])
    

    n_white_pix_adapt = np.sum(mask_largest_adapt[0] == 255)
    if n_white_pix_adapt > threshold_whites:
        print(Fore.GREEN + 'Object found!' + Fore.RESET)
        cv2.imwrite('/home/nunocunha99/Desktop/GitHub/PSR_TP3/object_found.jpg', cv_image)
        print(Fore.RED + 'This object has just been photographed' + Fore.RESET)
        object_publisher.publish(True)
        rate.sleep()
    elif n_white_pix_adapt < threshold_whites:
        object_publisher.publish(False)
        rate.sleep()

    n_white_pix_spherev = np.sum(mask_largest_spherev[0] == 255)
    if n_white_pix_spherev > threshold_whites:
        print(Fore.GREEN + 'Violet sphere found!' + Fore.RESET)
        cv2.imwrite('/home/nunocunha99/Desktop/GitHub/PSR_TP3/violet_sphere_found.jpg', cv_image)
        print(Fore.RED + 'The violet sphere has just been photographed' + Fore.RESET)
        sphere_publisher.publish(True)
        rate.sleep()
    elif n_white_pix_spherev < threshold_whites:
        sphere_publisher.publish(False)
        rate.sleep()


    frame = imutils.resize(cv_image, width=min(400, cv_image.shape[1]))
    (regions, _) = hog.detectMultiScale(frame, 
                                    winStride=(4, 4),
                                    padding=(4, 4),
                                    scale=1.05)

    if len(regions) > 0:
        print(Fore.RED + 'Found someone!' + Fore.RESET)
        people_publisher.publish(True)
        rate.sleep()
    
    elif len(regions) == 0:
        people_publisher.publish(False)
        rate.sleep()

    for (x, y, w, h) in regions:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    

    # Display the resulting frame
    cv2.imshow(window_name4, frame)


    

    

    pressed_key = cv2.waitKey(1)

    
def main():

    global people_publisher, object_publisher, sphere_publisher, rate

    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(window_name2, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(window_name3, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(window_name4, cv2.WINDOW_AUTOSIZE)

    cv2.setMouseCallback(window_name,mouse)

    # Initialization of a ros node
    rospy.init_node('camera_subscriber', anonymous=True)

    # Init the subscriber
    rospy.Subscriber('/camera/rgb/image_raw', Image, msgReceivedCallback)

    people_publisher = rospy.Publisher('people_info', Bool, queue_size=10)
    object_publisher = rospy.Publisher('object_info', Bool, queue_size=10)
    sphere_publisher = rospy.Publisher('sphere_info', Bool, queue_size=10)
    rate = rospy.Rate(100)



    # ------------------------------------
    # Execution 
    # ------------------------------------
    rospy.spin()

    # ------------------------------------
    # Termination 
    # ------------------------------------

if __name__ == '__main__':
    main()