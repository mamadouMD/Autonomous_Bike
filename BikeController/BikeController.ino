unsigned long prev;
unsigned long now;

void setup() {  
  bikespeedinit();
  bikedirectioninit();
  bikebrakeinit();
  compassinit();
  Serial.begin(115200);

  Serial.println("Arduino code started up");

  prev = millis();
}

int curr = 0;
int incomingByte;
void loop() {
  /*
  if (Serial.available() > 0) {
    incomingByte = Serial.read();

    if(incomingByte == 49) {
      Serial.println("Got 1");
      curr = 1;  
    } else if(incomingByte == 48) {
      Serial.println("Got 0");
      curr = 0;
    }
  } else {
    Serial.println("No Serial available");
  }

  if(curr == 1) {
    bikeunbrake();
    bikedirection(-30);
    bikespeed(10);    
  } else {
    bikebrake();
    bikedirection(30);
    bikespeed(0);       
  }
  delay(1);
  */

  now = millis();

  if (now-prev >= 1000) {
    prev = now;
    send_compass_data();
  }
  
  wait_for_command();
}
