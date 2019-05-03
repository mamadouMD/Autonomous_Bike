void setup() {  
  bikespeedinit();
  bikedirectioninit();
  bikebrakeinit();
  Serial.begin(115200);

  Serial.println("Arduino code started up");
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
    bikedirection(90);
    bikespeed(10);    
  } else {
    bikebrake();
    bikedirection(90);
    bikespeed(0);       
  }
  delay(1);
  */
  wait_for_command();
}
