#include <math.h>

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
  
}
