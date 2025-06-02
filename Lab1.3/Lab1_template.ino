// -------------------------------------------
//
//  Poject: Lab1_task1
//  Group:
//  Students:
//  Date:
//  ------------------------------------------

#define OFF 0
#define ON 1
int incomingByte;

// put your setup code here
void setup() {

  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);

  // initialize serial port and wait for port to open:
  Serial.begin(9600);

  // wait for serial port to connect. Needed for native USB port only
  while (!Serial1) {} 
  
  // init digital IO pins
  digitalWrite(LED_BUILTIN, LOW); 
}


// put your main code here
void loop() {
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    if (incomingByte == 'N') {
      digitalWrite(LED_BUILTIN, ON);
    }
    if (incomingByte == 'F') {
      digitalWrite(LED_BUILTIN, OFF);
    }
    if (incomingByte == 'B') {
      while (incomingByte == 'B' || incomingByte != 'N' && incomingByte != 'F') {
        digitalWrite(LED_BUILTIN, ON);
        delay(1000);
        digitalWrite(LED_BUILTIN, OFF);
        delay(1000);
        incomingByte = Serial.peek();
      }
    }
  }
}
