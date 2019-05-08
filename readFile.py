#  This script is use to create a json data file. the json data form is
#  one of the most data form used nowdays. 
# 
# input : data file .gpx
# output: outpyt.js
# 
# Author: MAMADOU DIALLO 

import json
import math as Math
import re

match_patern = r"[-+]?\d*\.\d+|\d+"

data = {}  

data['coordonate'] = []
data['detail'] = []

# Computing the distance between two given GPS point
#
# Haversine
# formula:    a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
#             c = 2 ⋅ atan2( √a, √(1−a) )
#             d = R ⋅ c
#           
#           where   φ is latitude, λ is longitude, R is earth’s radius (mean radius = 6,371km);
#           note that angles need to be in radians to pass to trig functions!

def distance(lon1, lat1, lon2, lat2):
    
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
def bearing(lon1, lat1, lon2, lat2):
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
def midPoint(lon1, lat1, lon2, lat2):
    lon1 = Math.radians(lon1)
    lon2 = Math.radians(lon2)
    lat1 = Math.radians(lat1)
    lat2 = Math.radians(lat2)

    Bx = Math.cos(lat2) * Math.cos(lon2-lon1);
    By = Math.cos(lat2) * Math.sin(lon2-lon1);
    phi3 = Math.atan2(Math.sin(lat1) + Math.sin(lat2), Math.sqrt( (Math.cos(lat1)+Bx)*(Math.cos(lat1)+Bx) + By*By ) );

    lamdha3 = lon1 + Math.atan2(By, Math.cos(lat1) + Bx);

    return [phi3, lamdha3]



strs = "<trkpt lat="
with open ('GPS/BeoE_Stamp1.gpx', 'rt') as myfile:  # Open file lorem.txt for reading text
    for myline in myfile:                 # For each line, read it to a string 
        #str.startswith(str, beg=0,end=len(string));
        #if myline.lstrip(' ').startswith(myline.lstrip(' '), beg=0, end=len(str):
        if strs in myline.lstrip(' '):
        	#print(myline)                 # print that string, repeat
        	sp = myline.split()
        	# print(sp[1][4:])
        	# print(sp[2][4:(len(sp[2])-2)])
        	data['coordonate'].append({  
			    'lat': re.findall(match_patern, sp[1][4:]),
			    'lon': re.findall(match_patern, sp[2][4:(len(sp[2])-2)]),
                
			})

			#print(data):
i = 0
for p in data['coordonate']:
    if (i == 0) :
        lat1 = float(p['lat'][0])
        lon1 = float(p['lon'][0])
        i = i + 1
    else:
        lon2 = float(p['lon'][0])
        lat2 = float(p['lat'][0])

        bring = bearing(lon1, lat1, lon2, lat2)
        dist  = distance(lon1, lat1, lon2, lat2)

        initial_Bearing = (bring + 360)% 360
        final_bearing = (bring + 180) % 360

        midPoint1 = midPoint(lon1, lat1, lon2, lat2)

        data['detail'].append({
            'distance': dist,
            'initial_Bearing': initial_Bearing,
            'final_bearing': final_bearing,
            'midPoint': midPoint1
        })

        lon1 = lon2
        lat1 = lat2
    


with open('data.js', 'w') as outfile:  
    json.dump(data, outfile)

with open('data.js') as json_file:  
    data = json.load(json_file)
    for p, w in zip(data['coordonate'], data['detail']):
        print('lat: ' + p['lat'][0])
        print('lon: ' + p['lon'][0])
        print('initial_Bearing: '+ str(w['initial_Bearing']))
        print('final_bearing: ' + str(w['final_bearing']))
        print('Mid Point: ')
        print('     lat:' + str(w['midPoint'][0]))
        print('     lon:' + str(w['midPoint'][1]))
        print(' ')





















