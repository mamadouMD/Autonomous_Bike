import time
import bike_ultimate_gps

gps = bike_ultimate_gps.UltimateGPS()

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
    if current - last_print >= 1.0:
        last_print = current
        print(gps.get_gps_coord())