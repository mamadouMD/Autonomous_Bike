#!/bin/python3


import sys
import serial
import serial.tools.list_ports

import threading
import time

BAUD = 115200

class NavigationThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def get_port(self):
        ports = serial.tools.list_ports.grep('USB')
        port = None

        for p in ports:
            port = p

        print(str(port))
        return port

    def connect(self):
        port = self.get_port()
        if port:
            return serial.Serial(port.device, BAUD, timeout=2)
        else:
            print("Arduino not found! Is it connected?")
            return None
    
    def go(self):
        self.okay = True

    
    def stop(self):
        self.okay = False
        

    def run(self):
        self.ser = self.connect()
        if (self.ser):
            print("Connected to Arduino!!!!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            i = 0
            while 1:
                print("*****Serial Loop iteration.... " + str(i));
                i = i + 1
                time.sleep(.25)
                print("out waiting: " + str(self.ser.out_waiting) )
                if self.ser.out_waiting == 0:
                    if self.okay:
                        print("~~~~~sending one")
                        self.ser.write("1".encode('utf-8'))
                    else:
                        print("~~~~~sending zero")
                        self.ser.write("0".encode('utf-8'))

                if self.ser.in_waiting > 0:
                    try:
                        print("Arduino says:")
                        print((self.ser.read(self.ser.in_waiting)).decode('utf-8'), end =" ") 
                    except:
                        None

