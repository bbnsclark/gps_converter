#!/usr/bin/python

import time
import numpy as np
from datetime import datetime
from math import pi, cos, sin

import tf
import rospy
#from gps_driver.msg import GPSQual
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import Int32
from nav_msgs.msg import Odometry
from gps_common.msg import GPSFix
from geometry_msgs.msg import Quaternion, Twist

class Node:

    def __init__(self):

        rospy.init_node("GPSCONV")

        rospy.on_shutdown(self.shutdown)

        rospy.loginfo("Starting GPS convertion...")

        self.rate = 1.0
        
        self.heading = 0.0
        
        self.latitude = 0.0
        
        self.altitude = 0.0
        
        self.longitude = 0.0
        
        self.pub_gps_fix = rospy.Publisher('gps_fix', GPSFix, queue_size = 1)

        self.pub_gps_initial_fix = rospy.Publisher('gps_initial_fix', GPSFix, queue_size = 1, latch = True)
        
        self.sub_gps_navsat = rospy.Subscriber('gps_navsat', NavSatFix, self.gps_navsat_callback)
        
        self.sub_gps_heading = rospy.Subscriber('gps_heading', Int32, self.gps_heading_callback)
        
        self.gps_msg = GPSFix()

        self.count = 0


    def run(self):

        rospy.loginfo("Starting GPS broadcast")

        r_time = rospy.Rate(self.rate)

        while not rospy.is_shutdown():

            # building the GPS Fix message
            self.gps_msg.header.stamp = rospy.Time.now()

            self.gps_msg.header.frame_id = 'base_link'   

            self.gps_msg.latitude = self.latitude
   
            self.gps_msg.longitude = self.longitude
   
            self.gps_msg.altitude = self.altitude
   
            self.gps_msg.dip = self.heading

            # publishing            
            self.pub_gps_fix.publish(self.gps_msg)

            if self.count == 0:

                self.pub_gps_initial_fix.publish(self.gps_msg) 

                self.count = 1 

            r_time.sleep()


    def gps_heading_callback(self, msg):

        self.heading = msg.data


    def gps_navsat_callback(self, msg):

        self.latitude = msg.latitude

        self.longitude = msg.longitude

        self.altitude = msg.longitude


    def shutdown(self):

        pass
    
        
if __name__ == "__main__":

    try:

        node = Node()

        node.run()

    except rospy.ROSInterruptException:

        pass

    rospy.loginfo("Exiting")
