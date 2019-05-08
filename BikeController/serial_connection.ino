
void wait_for_command() {
  int first_byte;
  int second_byte;
  if(Serial.available() >0) {
    first_byte = Serial.read();
    send_info("First byte " + String(first_byte));
    if(first_byte == 0xB1) {
      second_byte = read_serial();
      send_info("Second byte " + String(second_byte));
      if(second_byte == 0xCE) {
        send_info("Got a message");
        read_msg();
      }
    }
  } else {
    //send_info("No serial available");
  }
}

void read_msg() {
  int type;
  int speed;
  int braking;
  type = read_serial();

  switch(type) {
    case 0x00:
      send_info("Got a speed command");
      speed = read_serial();
      send_info("Recieved this speed: " + String(speed)); 
      bikespeed(speed);
      break;
    case 0x01:
      send_info("Got a brake command");
      braking = read_serial();
      send_info("Recieved this brake: " + String(braking));
      //Fix this later to variable break hardness
      switch(braking) {
        case 1:
          bikebrake();
          break;
        case 2:
          bikebrake();
          break;
        case 3:
          bikeunbrake();
          break;
        default:
          bikebrake();
          break;
      }
      break;
    case 0x02:
      send_info("Got a steer command"); 
      uint16_t steerb;
      Serial.readBytes((byte*)&steerb,2);
      send_info("Recieved this steer: " + String(steerb));
      bikedirection((int)steerb);
      break;
    case 0x03:
      send_info("Got a heading, error");
      break;
    case 0x04:
      send_info("Got some info, error");
      break;
    default:
      send_info("Got unknown type, error");
      break;
  }
}

void send_info(String info) {
  int first_byte = 0xB1;
  int second_byte = 0xCE;

  int len = info.length()+1;
  byte infob[256];
  info.getBytes(infob,len);
  
  Serial.write(first_byte);
  Serial.write(second_byte);
  Serial.write(0x04);
  
  Serial.write(len);
  Serial.write(infob, len);
}

void send_compass_data() {
  int first_byte = 0xB1;
  int second_byte = 0xCE;
  
  Serial.write(first_byte);
  Serial.write(second_byte);
  Serial.write(0x03);
  
  double heading = get_heading();
  
  String serial_data="";
  
  serial_data = String(heading,5);
  int len = serial_data.length();
  byte serial_datab[256];
  serial_data.getBytes(serial_datab,len);
  
  Serial.write(serial_datab, len);
}

int read_serial() {
  while(Serial.available() <= 0) {}
  return Serial.read();
}
