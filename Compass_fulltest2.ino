#include <math.h>
#include <Wire.h>
#include <LSM303.h>

/* Assign a unique ID to this sensor at the same time */ 
 LSM303 compass;

const float alpha = 0.15;
float fXa = 0;
float fYa = 0;
float fZa = 0;
float fXm = 0;
float fYm = 0;
float fZm = 0;

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
  int approx1;
  int approx2;

void setup() {

Serial.begin(9600);
Wire.begin();
compass.init();
compass.enableDefault();

  Serial.begin(9600);
  Serial.println("Magnetometer Test"); Serial.println("");
  
  /* Initialise the sensor */

  lat1 = 49.243824;
  lat2 = 49.235347;
  long1 = -121.887340;
  long2 = -121.92532;

  approx1 = 0;
  approx2 = 0;

  y = sin(long2 - long1) * cos(lat2);

  Serial.println(y);
  x = cos(lat1) * sin(lat2)- sin(lat1) * cos(lat2) * cos(long2-long1);

    polar = atan2(y, x);
    angle = (polar * 4068)/71;
    coterminal = (angle + 360) % 360;
    Serial.print("Compass Heading:  ");
    Serial.println(coterminal);
}



void loop()
{
compass.read();
float pitch, pitch_print, roll, roll_print, Heading, Xa_off, Ya_off, Za_off, Xa_cal, Ya_cal, Za_cal, Xm_off, Ym_off, Zm_off, Xm_cal, Ym_cal, Zm_cal, fXm_comp, fYm_comp;

// Accelerometer calibration
Xa_off = compass.a.x/16.0 + 6.008747;
Ya_off = compass.a.y/16.0 - 18.648762;
Za_off = compass.a.z/16.0 + 10.808316;
Xa_cal =  0.980977*Xa_off + 0.001993*Ya_off - 0.004377*Za_off;
Ya_cal =  0.001993*Xa_off + 0.998259*Ya_off - 0.000417*Za_off;
Za_cal = -0.004377*Xa_off - 0.000417*Ya_off + 0.942771*Za_off;

// Magnetometer calibration
Xm_off = compass.m.x*(100000.0/1100.0) - 8397.862881;
Ym_off = compass.m.y*(100000.0/1100.0) - 3307.507492;
Zm_off = compass.m.z*(100000.0/980.0 ) + 2718.831179;
Xm_cal =  0.469042*Xm_off + -0.003955*Ym_off + 0.004072*Zm_off; //X-axis correction for combined scale factors (Default: positive factors)
Ym_cal =  -0.003955*Xm_off + 0.468365*Ym_off + -0.001912*Zm_off; //Y-axis correction for combined scale factors
Zm_cal = 0.004072*Xm_off + -0.001912*Ym_off + 0.426844*Zm_off; //Z-axis correction for combined scale factors

// Low-Pass filter accelerometer
fXa = Xa_cal * alpha + (fXa * (1.0 - alpha));
fYa = Ya_cal * alpha + (fYa * (1.0 - alpha));
fZa = Za_cal * alpha + (fZa * (1.0 - alpha));

// Low-Pass filter magnetometer
fXm = Xm_cal * alpha + (fXm * (1.0 - alpha));
fYm = Ym_cal * alpha + (fYm * (1.0 - alpha));
fZm = Zm_cal * alpha + (fZm * (1.0 - alpha));

// Pitch and roll
roll  = atan2(fYa, sqrt(fXa*fXa + fZa*fZa));
pitch = atan2(fXa, sqrt(fYa*fYa + fZa*fZa));
roll_print = roll*180.0/M_PI;
pitch_print = pitch*180.0/M_PI;

// Tilt compensated magnetic sensor measurements
fXm_comp = fXm*cos(pitch)+fZm*sin(pitch);
fYm_comp = fXm*sin(roll)*sin(pitch)+fYm*cos(roll)-fZm*sin(roll)*cos(pitch);

// Arctangent of y/x
Heading = (atan2(fYm_comp,fXm_comp)*180.0)/M_PI;
if (Heading < 0)
Heading += 360;
Serial.print("Heading: "); Serial.println(Heading);
delay(250);
}
