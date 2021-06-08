#!/usr/bin/env python

from gazebo_msgs.srv import GetModelState
import rospy

class Box:
    def __init__(self, model_name, relative_entity_name):
        self._model_name = model_name
        self._relative_entity_name = relative_entity_name

class Depth_cam:
    def __init__(self, model_name, relative_entity_name):
        self._model_name = model_name
        self._relative_entity_name = relative_entity_name

class show_names:
    _objects = {
        "box": Box("cardboard_box", "link"),
        "depth_cam": Depth_cam("kinect_ros", "link"),
        #"depth_cam": Depth_cam("kinect_ros", "kinect_ros::kinect_ros::link"),
    }
    
    def show_gazebo_models(self):
        try:
            model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
            for object in self._objects.itervalues():
                resp_coordinates = model_coordinates(object._model_name, object._relative_entity_name)
                print(object._model_name)
                print(resp_coordinates.pose)
        except rospy.ServiceException as e:
            rospy.loginfo("Get model state not working: {0}".format(e))

if __name__ == "__main__":
    show = show_names()
    show.show_gazebo_models()
