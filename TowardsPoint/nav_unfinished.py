#Code to make the bike move toward a single gps point

import time
import bike_ultimate_gps
import coordinate_manipulation
import requests
import arduino
import geopy

class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError: status={}".format(self.status)

gps = bike_ultimate_gps.UltimateGPS()
coordm = coordinate_manipulation.CoordinateManipulation()
ard = arduino.Arduino()
ard.run()

destinationcoord = geopy.point.Point(38.99262,-76.9373,0)

last_print = time.monotonic()
while True:
    gps.gps_update()
    # Make sure to call gps.update() every loop iteration and at least twice
    # as fast as data comes from the GPS unit (usually every second).
    # This returns a bool that's true if it parsed new data (you can ignore it
    # though if you don't care and instead look at the has_fix property).
    #gps.update()
    # Every second print out current location details if there's a fix.
    current = time.monotonic()
    if current - last_print >= 3.0:
        last_print = current
        currcoord = gps.get_gps_coord()
        bearing = coordm.bearing(currcoord, destinationcoord)
        distance = coordm.bearing(currcoord, destinationcoord)

        jsonpost = {
            'longitude': currcoord.longitude,
            'latitude': currcoord.latitude,
            'deviceID': 123456
            }
        resp = requests.post('https://us-central1-fleet-8b5a9.cloudfunctions.net/sendPulse', json=jsonpost)

        if resp.status_code != 201 and resp.status_code != 200:
            raise ApiError('Post was not successful: {}'.format(resp.status_code))
        print('Sent GPS coordinate to Team 1')

        loc_data = {
            'name': 'The_Cool_One',
            'lat': str(currcoord.latitude),
            'lon': str(currcoord.longitude),
            'timestamp': 'Unk'
            }
        curr_time = time.gmtime()
        loc_data['timestamp'] = '{}/{}/{} {:02}:{:02}:{:02}'.format(
            curr_time.tm_mon,   # Grab parts of the time from the
            curr_time.tm_mday,  # struct_time object that holds
            curr_time.tm_year,  # the fix time.  Note you might
            curr_time.tm_hour,  # not get all data like year, day,
            curr_time.tm_min,   # month!
            curr_time.tm_sec)

        resp = requests.post('http://Fleetofbikes-env.vrqy7xh9wt.us-east-1.elasticbeanstalk.com/bike/location/', json=loc_data)

        if resp.status_code != 201 and resp.status_code != 200:
            raise ApiError('Post was not successful: {}'.format(resp.status_code))
        print('Sent GPS coordinate to Team 2')


        bike_heading = ard.getHeading()

        print("This is the bike bearing: ", bike_heading)
        print("This is the destination heading: ", bearing)
        #setSteer((bike_heading-bearing)-90)
