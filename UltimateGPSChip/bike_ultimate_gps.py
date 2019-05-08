# Will wait for a fix and print a message every second with the current location
# and other details.
import time
#import board
#import busio

import adafruit_gps
import geopy

# Define RX and TX pins for the board's serial port connected to the GPS.
# These are the defaults you should use for the GPS FeatherWing.
# For other boards set RX = GPS module TX, and TX = GPS module RX pins.
#RX = board.RXD
#TX = board.TXD

# Create a serial connection for the GPS connection using default speed and
# a slightly higher timeout (GPS modules typically update once a second).
#uart = busio.UART(TX, RX, baudrate=9600, timeout=3000)

# for a computer, use the pyserial library for uart access
import serial

class UltimateGPS:
    def __init__(self):
        self.uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3000)

        # Create a GPS module instance.
        self.gps = adafruit_gps.GPS(self.uart, debug=False)

        # Initialize the GPS module by changing what data it sends and at what rate.
        # These are NMEA extensions for PMTK_314_SET_NMEA_OUTPUT and
        # PMTK_220_SET_NMEA_UPDATERATE but you can send anything from here to adjust
        # the GPS module behavior:
        #   https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf

        # Turn on the basic GGA and RMC info (what you typically want)
        self.gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Turn on just minimum info (RMC only, location):
        #gps.send_command(b'PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Turn off everything:
        #gps.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Tuen on everything (not all of it is parsed!)
        #gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')

        # Set update rate to once a second (1hz) which is what you typically want.
        self.gps.send_command(b'PMTK220,1000')
        # Or decrease to once every two seconds by doubling the millisecond value.
        # Be sure to also increase your UART timeout above!
        #gps.send_command(b'PMTK220,2000')
        # You can also speed up the rate, but don't go too fast or else you can lose
        # data during parsing.  This would be twice a second (2hz, 500ms delay):
        #gps.send_command(b'PMTK220,500')
    
    def gps_update(self):
        self.gps.update()

    def get_gps_coord(self):
        last_print = time.monotonic()
        while not self.gps.has_fix:
            current = time.monotonic()
            if current - last_print >= 1.0:
                last_print = current
                if not self.gps.has_fix:
                    # Try again if we don't have a fix yet.
                    print('Waiting for fix...')
                    continue
                else:
                    break
        # We have a fix! (gps.has_fix is true)
        # Print out details about the fix like location, date, etc.
        print('=' * 40)  # Print a separator line.
        print('Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}'.format(
            self.gps.timestamp_utc.tm_mon,   # Grab parts of the time from the
            self.gps.timestamp_utc.tm_mday,  # struct_time object that holds
            self.gps.timestamp_utc.tm_year,  # the fix time.  Note you might
            self.gps.timestamp_utc.tm_hour,  # not get all data like year, day,
            self.gps.timestamp_utc.tm_min,   # month!
            self.gps.timestamp_utc.tm_sec))
        print('Latitude: {0:.6f} degrees'.format(self.gps.latitude))
        print('Longitude: {0:.6f} degrees'.format(self.gps.longitude))
        print('Fix quality: {}'.format(self.gps.fix_quality))
        # Some attributes beyond latitude, longitude and timestamp are optional
        # and might not be present.  Check if they're None before trying to use!
        if self.gps.satellites is not None:
            print('# satellites: {}'.format(self.gps.satellites))
        if self.gps.altitude_m is not None:
            print('Altitude: {} meters'.format(self.gps.altitude_m))
        if self.gps.speed_knots is not None:
            print('Speed: {} knots'.format(self.gps.speed_knots))
        if self.gps.track_angle_deg is not None:
            print('Track angle: {} degrees'.format(self.gps.track_angle_deg))
        if self.gps.horizontal_dilution is not None:
            print('Horizontal dilution: {}'.format(self.gps.horizontal_dilution))
        if self.gps.height_geoid is not None:
            print('Height geo ID: {} meters'.format(self.gps.height_geoid))
        #Build gps coord point
        return geopy.point.Point(latitude = self.gps.latitude,longitude = self.gps.longitude)


