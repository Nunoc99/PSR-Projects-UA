#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry

# -------------------- node init ---------------------- 
rospy.init_node('init_pose')
pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size = 1)

# --------------------- construct message -------------
init_msg = PoseWithCovarianceStamped()
init_msg.header.frame_id = "map"

# ---------- get initial pose from gazebo -------------
odom_msg = rospy.wait_for_message('/odom', Odometry)
init_msg.pose.pose.position.x = odom_msg.pose.pose.position.x
init_msg.pose.pose.position.y = odom_msg.pose.pose.position.y
init_msg.pose.pose.orientation.x = odom_msg.pose.pose.orientation.x
init_msg.pose.pose.orientation.y = odom_msg.pose.pose.orientation.y
init_msg.pose.pose.orientation.z = odom_msg.pose.pose.orientation.z
init_msg.pose.pose.orientation.w = odom_msg.pose.pose.orientation.w

rospy.sleep(1)

# ------------- publish message -----------------------
rospy.loginfo("Setting initial pose")
pub.publish(init_msg)
rospy.loginfo("Initial pose is set")


