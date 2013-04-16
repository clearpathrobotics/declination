#!/usr/bin/python

import geomag


gm = geomag.GeoMag("WMM.COF")
mag = gm.calc(43.411454, -80.472708)
print mag.dec
