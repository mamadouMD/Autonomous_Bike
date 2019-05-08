#!/usr/bin/env python3

import get_gps_points
import geopy

s = geopy.point.Point(-76.9373,38.99262,0)
f = geopy.point.Point(-76.94175,38.99139,0)

nodes = get_gps_points.get_nodes(s,f)
print(get_gps_points.get_coordinates(nodes))
