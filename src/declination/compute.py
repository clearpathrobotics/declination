#
#  @author     Mike Purvis <mpurvis@clearpathrobotics.com>
#  @copyright  Copyright (c) 2013, Clearpath Robotics, Inc.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     # Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     # Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     # Neither the name of Clearpath Robotics, Inc. nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL CLEARPATH ROBOTICS, INC. BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# Please send comments, questions, or patches to code@clearpathrobotics.com 


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
