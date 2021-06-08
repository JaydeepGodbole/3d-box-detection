#!/usr/bin/env python
#coding=utf-8

import rospy
import math
from gazebo_msgs.srv import *
import random
from geometry_msgs.msg import Point
from cv_bridge import CvBridge
import cv2

def normalize(dir):
    normalization_const = math.sqrt(dir.x**2 + dir.y**2 + dir.z**2)
    dir.x /= normalization_const
    dir.y /= normalization_const
    dir.z /= normalization_const
    return dir


def state_publisher():
    rospy.init_node('data_generator', anonymous = True)
    rospy.wait_for_service('/gazebo/set_model_state')
    set_state_service = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
    req = SetModelStateRequest()
    r = random.random()
    theta = random.random() * 2 * math.pi
    random_dir_cos = Point()
    random_dir_cos.x = r*math.cos(theta)
    random_dir_cos.y = r*math.sin(theta)
    random_dir_cos.z = math.sqrt(1 - r**2)

    # random_dir_cos.x = 0
    # random_dir_cos.y = 1
    # random_dir_cos.z = 0

    # We now have the direction cosines of the random viewing direction
    # We find the axis about which to turn the kinect as, the cross product between this direction and the original x axis

    rot_axis = Point()
    rot_axis.x = random_dir_cos.y*(0) - random_dir_cos.z*(0)
    rot_axis.y = -1*(random_dir_cos.x*(0) - random_dir_cos.z*(1))
    rot_axis.z = random_dir_cos.x*(0) - random_dir_cos.y*(1)
    rot_axis = normalize(rot_axis)
    print(rot_axis)

    # We now have the direction that we have to rotate the original coordinate axis about. Original angle is cosinverse of random_dir_cos.x.

    alpha = math.pi - math.acos(random_dir_cos.x)
    print(alpha)

    req.model_state.model_name = "kinect_ros"
    req.model_state.pose.position.x = random_dir_cos.x
    req.model_state.pose.position.y = random_dir_cos.y
    req.model_state.pose.position.z = random_dir_cos.z
    req.model_state.pose.orientation.w = math.cos(alpha/2)
    req.model_state.pose.orientation.x = math.sin(alpha/2)*rot_axis.x
    req.model_state.pose.orientation.y = math.sin(alpha/2)*rot_axis.y
    req.model_state.pose.orientation.z = math.sin(alpha/2)*rot_axis.z
    # req.model_state.pose.orientation.x = math.sin(alpha/2)*random_dir_cos.x
    # req.model_state.pose.orientation.y = math.sin(alpha/2)*random_dir_cos.y
    # req.model_state.pose.orientation.z = math.sin(alpha/2)*random_dir_cos.z
    
    req.model_state.twist.linear.x = 0
    req.model_state.twist.linear.y = 0
    req.model_state.twist.linear.z = 0
    req.model_state.twist.angular.x = 0
    req.model_state.twist.angular.y = 0
    req.model_state.twist.angular.z = 0
    req.model_state.reference_frame = 'world'

    result = set_state_service(req)

    bridge = CvBridge()

if __name__ == '__main__':
    try:
        state_publisher()
    except rospy.ROSInterruptException: pass