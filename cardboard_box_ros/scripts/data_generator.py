#!/usr/bin/env python


import rospy
import math
from gazebo_msgs.msg import ModelState

def state_publisher():
    pub = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=10)
    rospy.init_node('data_generator', anonymous = True)
    msg = ModelState()
    msg.model_name = 'kinect_ros'
    msg.pose.position.x = 1
    msg.pose.position.y = 0
    msg.pose.position.z = 0
    msg.pose.orientation.x = 0
    msg.pose.orientation.y = 0
    msg.pose.orientation.z = 0
    msg.pose.orientation.w = 1
    msg.twist.linear.x = 0
    msg.twist.linear.y = 0
    msg.twist.linear.z = 0
    msg.twist.angular.x = 0
    msg.twist.angular.y = 0
    msg.twist.angular.z = 0
    msg.reference_frame = 'world'

    if not rospy.is_shutdown():
        rospy.loginfo(msg)
        pub.publish(msg)

if __name__ == '__main__':
    try:
        state_publisher()
    except rospy.ROSInterruptException: pass