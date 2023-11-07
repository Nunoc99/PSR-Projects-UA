#!/usr/bin/env python3

import cv2
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from visualization_msgs.msg import Marker
from cv_bridge import CvBridge, CvBridgeError


def main():

    # init of a ros node
    rospy.init_node('rviz_publisher', anonymous=False)

    #create the publisher
    publisher = rospy.Publisher('~markers', Marker, queue_size=1)


    rate = rospy.Rate(1)
    while not rospy.is_shutdown():

        #create a marker
        marker = Marker()
        marker.header.frame_id = 'world'
        marker.ns = 'my_drawings'
        marker.id = 0
        marker.type = Marker.SPHERE
        marker.action = Marker.MODIFY

        marker.pose.position.x = 0
        marker.pose.position.y = 0
        marker.pose.position.z = 0

        marker.pose.orientation.x = 0
        marker.pose.orientation.y = 0
        marker.pose.orientation.z = 1
        marker.pose.orientation.w = 0

        marker.scale.x = 1
        marker.scale.y = 1
        marker.scale.z = 3

        marker.color.r = 0
        marker.color.g = 1
        marker.color.b = 0
        marker.color.a = 0.3

        marker.text = 'Not used'
        publisher.publish(marker)
        
        # Create a Cube marker
        marker = Marker()
        marker.header.frame_id = 'world'
        marker.ns = 'my_drawings'
        marker.id = 1
        marker.type = Marker.CUBE
        marker.action = Marker.MODIFY

        marker.pose.position.x = 0
        marker.pose.position.y = 0
        marker.pose.position.z = 0

        marker.pose.orientation.x = 0
        marker.pose.orientation.y = 0
        marker.pose.orientation.z = 1
        marker.pose.orientation.w = 0

        marker.scale.x = 0.3
        marker.scale.y = 0.3
        marker.scale.z = 0.3

        marker.color.r = 1
        marker.color.g = 0
        marker.color.b = 0
        marker.color.a = 1

        marker.text = 'Not used'
        publisher.publish(marker)
        
        # Create a text marker
        marker = Marker()
        marker.header.frame_id = 'world'
        marker.ns = 'my_drawings'
        marker.id = 2
        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.MODIFY

        marker.pose.position.x = 0
        marker.pose.position.y = 0
        marker.pose.position.z = 2

        marker.pose.orientation.x = 0
        marker.pose.orientation.y = 0
        marker.pose.orientation.z = 1
        marker.pose.orientation.w = 0

        marker.scale.x = 0.3
        marker.scale.y = 0.3
        marker.scale.z = 0.3

        marker.color.r = 1
        marker.color.g = 0
        marker.color.b = 1
        marker.color.a = 1

        marker.text = 'Arrival'

        #publisher the marker
        publisher.publish(marker)
        rate.sleep()

    # vid.release()


if __name__ == "__main__":
    main()