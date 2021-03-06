#!/usr/bin/env python    
'''
Created on Feb 21, 2013

@author: mllofriu
'''
import roslib; roslib.load_manifest('morris_simulation')
import rospy
import actionlib
from rospy.rostime import Duration
from trajectory_msgs.msg import JointTrajectoryPoint
import nao_msgs.msg
from naoqi import ALProxy

class JointMover(object):
    '''
    Method for moving a joint using ros
    '''

    def move(self, joint, pos, dur):
#        goal = nao_msgs.msg.JointTrajectoryGoal()
#        goal.trajectory.joint_names = [joint]
#        goal.trajectory.points.append(JointTrajectoryPoint(time_from_start = Duration(dur), positions = pos))
#        rospy.loginfo("Sending goal...")
#        self.client.send_goal(goal)
#        self.client.wait_for_result(Duration(1.0))
#        result = self.client.get_result()
#        if result != None:
#            rospy.loginfo("Results: %s", str(result.goal_position.position))
        self.motionProxy.angleInterpolation(joint, pos, dur, True)
        
    def __init__(self):        
        self.client = actionlib.SimpleActionClient("joint_trajectory", nao_msgs.msg.JointTrajectoryAction)
#        rospy.loginfo("Waiting for joint_trajectory and joint_stiffness servers...")
#        self.client.wait_for_server()
        try:
            self.motionProxy = ALProxy("ALMotion", "127.0.0.1", 9559)
        except Exception, e:
            print "Could not create proxy to ALMotion"
            print "Error was: ", e
        