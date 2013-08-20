from roslib.packages import get_pkg_dir
import rospy

from std_msgs.msg import Float32
from sensor_msgs.msg import NavSatFix

from geomag.geomag import GeoMag
from math import radians
from os import path


class Compute:
    def __init__(self):
        rospy.init_node("declination_provider")
        wmm_path = path.join(get_pkg_dir('declination'), "wmm", "WMM.COF")
        self.gm = GeoMag(wmm_path)

        self.fix = None
        self.sub = rospy.Subscriber("fix", NavSatFix, self._fix)
        self.pub = rospy.Publisher("declination", Float32, latch=True)

    def _fix(self, msg):
        if self.fix:
            # For now, return. Later, figure out conditions under which to recompute.
            return

        if msg.latitude and msg.longitude:
            self.fix = msg
            if not msg.altitude: msg.altitude = 0
            result = self.gm.calc(msg.latitude, msg.longitude, msg.altitude)
            result_rad = radians(result.dec)
            self.pub.publish(result_rad) 
            rospy.loginfo("Computed magnetic declination to be %f rad (%f degrees)" \
                % (result_rad, result.dec))

    def spin(self):
        rospy.spin()
