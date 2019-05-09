import arduino
import geopy
import time

ard = arduino.Arduino()
ard.run()

time.sleep(5)
ard.setSteer(270.56)
time.sleep(5)
ard.SetBreak(1)
time.sleep(5)
ard.SetSpeed(20)
