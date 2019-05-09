import arduino
import geopy

ard = arduino.Arduino()
ard.run()

ard.setSteer(270.56)
ard.SetBreak(1)
ard.SetSpeed(20)
