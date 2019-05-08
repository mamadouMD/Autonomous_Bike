#Code to make the bike move toward a single gps point

import time
import bike_ultimate_gps
import coordinate_manipulation

gps = bike_ultimate_gps.UltimateGPS()
coordm = coordinate_manipulation.CoordinateManipulation()

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
        
        if resp.status_code != 201:
            raise ApiError('Cannot post response: {}'.format(resp.status_code))
        print('Created task. ID: {}'.format(resp.json()["id"]))

        resp = todo.get_tasks()
        if resp.status_code != 200:
            raise ApiError('Cannot post: {}'.format(resp.status_code))
        for todo_item in resp.json():
            print('{} {}'.format(todo_item['id'], todo_item['summary']))
