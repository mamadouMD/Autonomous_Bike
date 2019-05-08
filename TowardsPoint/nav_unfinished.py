#Code to make the bike move toward a single gps point

import time
import bike_ultimate_gps
import coordinate_manipulation
import requests
import arduino

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
    if current - last_print >= 10.0:
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
        print('Sent GPS coordinate')

        bike_heading = ard.getHeading()

        print("This is the bike bearing: ", bike_heading)
        print("This is the destination heading: ", bearing)
        #setSteer((bike_heading-bearing)-90)
