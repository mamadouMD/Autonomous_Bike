import arduino
import geopy
import time

ard = arduino.Arduino()

time.sleep(1)
ard.setBreak(1)
time.sleep(1)
ard.setSteer(270.56)
time.sleep(1)
ard.setSpeed(20)
