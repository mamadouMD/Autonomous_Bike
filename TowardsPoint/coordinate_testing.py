import coordinate_manipulation
import geopy
from geopy import distance

coordm = coordinate_manipulation.CoordinateManipulation()

startcoord = geopy.point.Point(38.991485,-76.937277)
destinationcoord = geopy.point.Point(38.992615,-76.937294)

bearing = coordm.bearing(startcoord, destinationcoord)
distance = distance.distance(startcoord, destinationcoord).meters

print("This is the distance: ", distance)
print("This is the heading: ", bearing)
