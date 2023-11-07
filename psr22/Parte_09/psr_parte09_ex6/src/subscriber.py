#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

def msgReceivedCallback(msg):
    rospy.loginfo("I received " + str(msg.data))
    
def main():

    rospy.init_node('subscriber', anonymous=True)

    rospy.Subscriber('/chatter', String, msgReceivedCallback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    main()