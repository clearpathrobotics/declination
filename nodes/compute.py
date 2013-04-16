#!/usr/bin/env python

import roslib; roslib.load_manifest('declination')
import rospy

from std_msgs.msg import Float32
from sensor_msgs.msg import NavSatFix

from geomag.geomag import GeoMag


class Declination:
    def __init__(self):
        self.gm = GeoMag("../src/geomag/WMM.COF")
        rospy.init_node("declination_provider")

        self.fix = None
        self.sub = rospy.Subscriber("fix", NavSatFix, self._fix)
        self.pub = rospy.Publisher("declination", Float32, latch=True)

    def _fix(msg):
        if self.fix:
            # For now, return. Later, figure out conditions under which to recompute.
            return

        if msg.latitude and msg.longitude:
            self.fix = msg
            if not msg.altitude: msg.altitude = 0
            result = self.gm.calc(msg.latitude, msg.longitude, msg.altitude)
            self.pub.publish(result.dec) 

    def spin(self):
        rospy.spin()

if __name__ == "__main__":
    Declination().spin()
