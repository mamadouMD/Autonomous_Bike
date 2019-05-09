import arduino
import geopy
import time

ard = arduino.Arduino()

time.sleep(5)
ard.setBreak(3)
time.sleep(1)
ard.setSteer(0)
time.sleep(1)
ard.setSpeed(0)
