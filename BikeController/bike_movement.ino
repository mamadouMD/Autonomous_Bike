#include <SPI.h>
#include <Servo.h>

const int CS = 10;
int PotWiperVoltage = 1;
int RawVoltage = 0;
float Voltage = 0;

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
    int level = 68 + ((255-68)/speedsteps)*(speed);
    MCP41010Write(level);
    delay(100);
    RawVoltage = analogRead(PotWiperVoltage);
    Voltage = (RawVoltage * 5.0 )/ 1024.0;

    Serial.print("Level = " );                      
    Serial.print(level);      
    Serial.print("\t Voltage = ");
    Serial.println(Voltage,3);
  }
}

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
void bikedirection(int direction) {
  //1400 is max right (83)
  //1610 is center (104)
  //1820 is max left (125)
  int directionsteps = 210/(90-28);
  int val = 1610 - (direction - 90)*directionsteps;
  directionservo.writeMicroseconds(val);
}

void bikebrakeinit() {
  brakeservo.attach(6);
}

void bikebrake() {
  directionservo.write(170);
}

void bikeunbrake() {
  directionservo.write(100);
}

//void bikebrakemedium() {
  
//}

//void bikebrakehard() {
  
//}
