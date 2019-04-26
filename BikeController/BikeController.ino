void setup() {
  bikespeedinit();
  bikedirectioninit();
  bikebrakeinit();
  Serial.begin(9600);
}

void loop() {
  
  bikedirection(150);
  bikespeed(50);
}
