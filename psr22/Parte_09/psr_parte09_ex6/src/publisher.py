#!/usr/bin/env python3
# license removed for brevity
import rospy
from std_msgs.msg import String
from colorama import Fore, Style
import argparse

def main():

    # parser = argparse.ArgumentParser(description='')

    # parser.add_argument("-rp", "--run_publishers", required=False, default='chatter')
    # args = vars(parser.parse_args())

    rospy.init_node('publisher', anonymous=True)

    publisher = rospy.Publisher('/chatter', String, queue_size=10)

    frequency = rospy.get_param('/frequency')
    rate = rospy.Rate(frequency)

    while not rospy.is_shutdown():
        msg = "hello world " + str(rospy.get_time())

        highlight_text_color = rospy.get_param("/highlight_text_color")
        rospy.loginfo('Publishing ' + getattr(Fore, highlight_text_color) + msg + Style.RESET_ALL)
        publisher.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    main()
 