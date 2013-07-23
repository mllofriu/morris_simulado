'''
Created on Jun 27, 2013

@author: ludo
'''

class FloorFrameBroadcaster(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        rospy.init_node('turtle_tf_broadcaster')
        rospy.Subscriber('/torso',
                         turtlesim.msg.Pose,
                         handle_turtle_pose,
                         turtlename)
        rospy.spin()
        