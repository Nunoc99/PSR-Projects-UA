#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import argparse
from psr_parte08_ex4.msg import Dog

def msgReceivedCallback(msg):
    rospy.loginfo("I received\n" + str(msg) + '\n')
    
def main():

    parser = argparse.ArgumentParser(description='')

    parser.add_argument("-t", "--topic", required=False, default='chatter')
    args = vars(parser.parse_args())

    rospy.init_node('subscriber', anonymous=True)

    rospy.Subscriber(args['topic'], Dog, msgReceivedCallback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    main()