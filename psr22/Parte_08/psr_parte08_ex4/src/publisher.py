#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import argparse
from psr_parte08_ex4.msg import Dog

def main():

    parser = argparse.ArgumentParser(description='')

    parser.add_argument("-t", "--topic", required=False, default='chatter')
    parser.add_argument("-m", "--msg", required=False, default='Hello world')            
    parser.add_argument("-f", "--frequency", required=False, default=1)
    args = vars(parser.parse_args())

    dog = Dog()
    dog.name = 'Dalila'
    dog.color = 'brown'
    dog.age = 5
    dog.brothers.append('Zeus')
    dog.brothers.append('Rex')

    rospy.init_node('publisher', anonymous=True)

    publisher = rospy.Publisher(args['topic'], Dog, queue_size=10)

    rate = rospy.Rate(args['frequency']) 

    while not rospy.is_shutdown():

        rospy.loginfo('Pubishing ' + str(dog))
        publisher.publish(dog)
        rate.sleep()

if __name__ == '__main__':
    main()
 