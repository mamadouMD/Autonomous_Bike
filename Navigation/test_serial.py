import arduino
import geopy
import time

ard = arduino.Arduino()

time.sleep(5)
ard.setBrake(3)
time.sleep(1)
ard.setSteer(30)
time.sleep(1)
ard.setSpeed(10)
