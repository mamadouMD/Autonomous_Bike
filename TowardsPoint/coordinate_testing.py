import coordinate_manipulation
import geopy


startcoord = geopy.point.Point(38.991485,-76.937277)
destinationcoord = geopy.point.Point(38.992615,-76.937294)

bearing = coordm.bearing(currcoord, destinationcoord)
distance = coordm.bearing(currcoord, destinationcoord)

print("This is the bike bearing: ", bike_heading)
print("This is the destination heading: ", bearing)
