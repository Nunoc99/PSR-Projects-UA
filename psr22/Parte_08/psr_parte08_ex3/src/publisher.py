#!/usr/bin/env python3
# license removed for brevity
import rospy
from std_msgs.msg import String

def main():
    rospy.init_node('publisher', anonymous=True)

    publisher = rospy.Publisher('chatter', String, queue_size=10)
    rate = rospy.Rate(1) 
    while not rospy.is_shutdown():
        msg = "hello world " + str(rospy.get_time())
        rospy.loginfo('Publishing ' + msg)
        publisher.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    main()
 