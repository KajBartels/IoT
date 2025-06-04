// -------------------------------------------
//
//  Poject: Lab1_task1
//  Group:
//  Students:
//  Date:
//  ------------------------------------------
#include <Arduino_LSM6DS3.h>

float x,y,z;

// put your setup code here
void setup() {
  // initialize serial port and wait for port to open:
  Serial.begin(9600);

  // wait for serial port to connect. Needed for native USB port only
  while (!Serial1) {} 

  if(!IMU.begin()){
    Serial.println("Failed to initialize IMU");
    while(1);
  }
  
}


// put your main code here
void loop() {
  if (Serial.available() > 0) {
    if (IMU.accelerationAvailable()) {
        IMU.readAcceleration(x, y, z);
        Serial.print(x);
        Serial.print('\t');
        Serial.print(y);
        Serial.print('\t');
        Serial.println(z);

    }
  }
  delay(1000);
}