#include <SPI.h>
#include <Servo.h>

const int CS = 10;
int PotWiperVoltage = 1;
int RawVoltage = 0;
float Voltage = 0;
int level = 0;

Servo directionservo;
Servo brakeservo;

void bikespeedinit() {
  pinMode (CS, OUTPUT);   
  SPI.begin();
}

//Can input speed from 0 to steps(100 at the moment)
void bikespeed(int speed) {
  int speedsteps = 100;
  if(speed == 0) {
    MCP41010Write(speed);
    delay(100);
    RawVoltage = analogRead(PotWiperVoltage);
    Voltage = (RawVoltage * 5.0 )/ 1024.0;
  } else {
    level = 68 + ((double)(240-68)/speedsteps)*(speed);
    MCP41010Write(level);
    delay(100);
    RawVoltage = analogRead(PotWiperVoltage);
    Voltage = (RawVoltage * 5.0 )/ 1024.0;

    send_info("Level = " );                      
    send_info(String(level));      
    send_info("\t Voltage = ");
    send_info(String(Voltage,3));
  }
}

/*
void bikespeed(int speed) {
  if(speed == 0) {
    analogWrite(3,0);   
  } else {
    analogWrite(3,100); 
  }
  
  RawVoltage = analogRead(PotWiperVoltage);
  Voltage = (RawVoltage * 5.0 )/ 1024.0;

  send_info("\t Voltage = ");
  send_info(String(Voltage,3));
}*/

void MCP41010Write(byte value) 
{
  // Note that the integer vale passed to this subroutine
  // is cast to a byte
  
  digitalWrite(CS,LOW);
  SPI.transfer(B00010001); // This tells the chip to set the pot
  SPI.transfer(value);     // This tells it the pot position
  digitalWrite(CS,HIGH); 
}

void bikedirectioninit() {
  directionservo.attach(9);
}

/*Eventually write it so that the turn is less sudden*/

//Input beteween 0 and 180
void bikedirection(double direction) {
  //1230 is max right (83)
  //1420 is center (104)
  //1610 is max left (125)
  if(direction > 62) {
    direction = 62.0;
  } else if (direction < -62) {
    direction = -62.0;
  }
  double directionsteps = ((double)(1420-1260)/62);
  int val = 1420 - (direction)*directionsteps;
  directionservo.writeMicroseconds(val);
}

void bikebrakeinit() {
  brakeservo.attach(6);
}

void bikebrake() {
  directionservo.write(170);
  send_info("Braking the bike");
}

void bikeunbrake() {
  directionservo.write(100);
  send_info("Unbraking the bike");
}

//void bikebrakemedium() {
  
//}

//void bikebrakehard() {
  
//}
