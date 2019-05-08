#include <math.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM303_U.h>

/* Assign a unique ID to this sensor at the same time */
Adafruit_LSM303_Mag_Unified mag = Adafruit_LSM303_Mag_Unified(12345);
 

  double y;
  double x;
  double lat1;
  double lat2;
  double long1;
  double long2;
  double bring;
  double polar;
  int angle;
  int coterminal;

void setup() {


  Serial.begin(9600);
  Serial.println("Magnetometer Test"); Serial.println("");
  
  /* Initialise the sensor */
  if(!mag.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
    Serial.println("Ooops, no LSM303 detected ... Check your wiring!");
    while(1);
  }


  lat1 = 49.243824;
  lat2 = 49.235347;
  long1 = -121.887340;
  long2 = -121.92532;

  y = sin(long2 - long1) * cos(lat2);

  Serial.println(y);
  x = cos(lat1) * sin(lat2)- sin(lat1) * cos(lat2) * cos(long2-long1);

    polar = atan2(y, x);
    angle = (polar * 4068)/71;
    coterminal = (angle + 360) % 360;
    Serial.print("Compass Heading:  ");
    Serial.println(coterminal);


}

void loop() {

    /* Get a new sensor event */ 
  sensors_event_t event; 
  mag.getEvent(&event);
  
  float Pi = 3.14159;
  
  // Calculate the angle of the vector y,x
  float heading = (atan2(event.magnetic.y,event.magnetic.x) * 180) / Pi;
  
  // Normalize to 0-360
  if (heading < 0)
  {
    heading = 360 + heading;
  }

  
  Serial.print("Compass Heading: ");
  Serial.println(heading);


 if (heading < coterminal){
  Serial.println("turn right \n");
 }

 else if (heading > coterminal){
  Serial.println("turn left \n");
 }

  delay(1050);
}
