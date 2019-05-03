#!/bin/python3


import sys
import serial
import serial.tools.list_ports

import threading
import time
import struct

BAUD = 115200

class Arduino(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.ser = self.start()
        self.okay = True
        self.heading = 0


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
    
    def getHeading(self):
        return self.heading

    def sendMagic(self):
        self.ser.write(b'\xB1')
        self.ser.write(b'\xce')

    def setSpeed(self, speed):
        try:
            self.sendMagic()
            self.ser.write(b'\00')
            print(bytes([speed]))
            self.ser.write(bytes([speed]))
        except Error as e:
            print("******Failed to send to arduino!**** Error: " + str(e))

    def setBreak(self, brk):
        try:
            self.sendMagic()
            self.ser.write(b'\01')
            self.ser.write(bytes([speed]))
        except Error as e:
            print(e)
            print("******Failed to send to arduino!****: " + str(e))

    def setSteer(self, steer):
        try:
            self.sendMagic()
            self.ser.write(b'\02')
            data = struct.pack(steer, "<H")
            self.ser.write(data)
        except:
            print("******Failed to send to arduino!****")

    def recvCommand(self):
        b = self.ser.read()
        if b == b'\xb1':
            b = self.ser.read()
            if b == b'\xce':
                return self.ser.read()
        return None
        

    def run(self):
        self.ser = self.connect()
        if (self.ser):
            print("Connected to Arduino!!!!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            while 1:
                if self.ser.in_waiting > 0:
                    try:
                        comm = self.recvCommand()
                        if comm:
                            if comm == b'\x03':
                                heading_len = int.from_bytes(self.ser.read(),"little")
                                heading_str = self.ser.read(heading_len).decode('utf-8')
                                self.heading = float(heading_str)
                            elif comm == b'\x04':
                                info_len = int.from_bytes(self.ser.read(),"little")
                                msg = self.ser.read(info_len).decode('utf-8')
                                print("Arduino: " + msg)
                            else:
                                print("Unknown Command from Arduino!")
                    except Exception as e:
                        print("*** Failed to read from ardino")
                        print(e)
                        None
