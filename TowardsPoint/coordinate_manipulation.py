import json
import math as Math
import re
import geopy

class CoordinateManipulation:
    def __init__(self):
        return
    # Computing the distance between two given GPS point
    #
    # Haversine
    # formula:    a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
    #             c = 2 ⋅ atan2( √a, √(1−a) )
    #             d = R ⋅ c
    #
    #           where   φ is latitude, λ is longitude, R is earth’s radius (mean radius = 6,371km);
    #           note that angles need to be in radians to pass to trig functions!
    def distance(self, coord1, coord2):
        lon1 = coord1.longitude
        lat1 = coord1.latitude
        lon2 = coord2.longitude
        lat2 = coord2.latitude
        R = 6371e3; # metres
        phi1 = Math.radians(lat1)
        phi2 = Math.radians(lat2)
        delta_phi = Math.radians( lat2-lat1 );
        delta_lamdha = Math.radians( lon2-lon1 );

        a = Math.sin(delta_phi/2) * Math.sin(delta_phi/2) + Math.cos(phi1) * Math.cos(phi2) * Math.sin(delta_lamdha/2) * Math.sin(delta_lamdha/2);

        c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

        d = R * c

        return d

    # Computing the bearing from long and lat of two GPS coordonate
    #
    # Formula:    θ = atan2( sin Δλ ⋅ cos φ2 , cos φ1 ⋅ sin φ2 − sin φ1 ⋅ cos φ2 ⋅ cos Δλ )
    #             where   φ1,λ1 is the start point, φ2,λ2 the end point (Δλ is the difference in longitude)
    def bearing(self, coord1, coord2):
        lon1 = coord1.longitude
        lat1 = coord1.latitude
        lon2 = coord2.longitude
        lat2 = coord2.latitude
        lon1 = Math.radians(lon1)
        lon2 = Math.radians(lon2)
        lat1 = Math.radians(lat1)
        lat2 = Math.radians(lat2)

        y = Math.sin(lat2-lat1) * Math.cos(lat2)
        x = Math.cos(lat1)*Math.sin(lat2) - Math.sin(lat1)*Math.cos(lat2)*Math.cos(lon2-lon1)

        bearing = Math.degrees( Math.atan2(y, x) )

        return bearing

    # Since atan2 returns values in the range -π ... +π (that is, -180° ... +180°), to normalise the result
    # to a compass bearing (in the range 0° ... 360°, with −ve values transformed into the range 180° ... 360°),
    # convert to degrees and then use (θ+360) % 360, where % is (floating point) modulo.

    # initial_Bearing = (bearing + 360)% 360

    # For final bearing, simply take the initial bearing from the end point to the start point and
    # reverse it (using θ = (θ+180) % 360).

    # final_bearing = (bearing + 180) % 360

    # Computing the half point between the two GPS coordonate
    def midPoint(self, coord1, coord2):
        lon1 = coord1.longitude
        lat1 = coord1.latitude
        lon2 = coord2.longitude
        lat2 = coord2.latitude
        lon1 = Math.radians(lon1)
        lon2 = Math.radians(lon2)
        lat1 = Math.radians(lat1)
        lat2 = Math.radians(lat2)

        Bx = Math.cos(lat2) * Math.cos(lon2-lon1);
        By = Math.cos(lat2) * Math.sin(lon2-lon1);
        phi3 = Math.atan2(Math.sin(lat1) + Math.sin(lat2), Math.sqrt( (Math.cos(lat1)+Bx)*(Math.cos(lat1)+Bx) + By*By ) );

        lamdha3 = lon1 + Math.atan2(By, Math.cos(lat1) + Bx);

        return [phi3, lamdha3]

    def calculate_initial_compass_bearing(self, pointA, pointB):
    """
    Calculates the bearing between two points.

    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))

    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees

    :Returns:
      The bearing in degrees

    :Returns Type:
      float
    """

    lat1 = math.radians(pointA.latitude)
    lat2 = math.radians(pointB.latitude)

    diffLong = math.radians(pointB.longitude - pointA.longitude)

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing
