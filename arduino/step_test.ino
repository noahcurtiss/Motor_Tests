#include "Wire.h"
const byte ledPin = 13;
const byte interruptPin = 2;
volatile byte state = LOW;
volatile int timeold;
volatile int rpm= 0;
volatile int dt= 0;
int sensorValue, force;
int cmd = 10, max_cmd=250, cmd_step=10;
int t_rest = 20000, t_run=7000,t;  //in roughly ms
int incomingByte = 0;
int analogPin = 0; 
int val = 0;
#define TWI_BLCTRL_BASEADDR 0x52
#define TWI_BLCTRL_BASEADDR_READ 0x52

void setup() {
  Wire.begin();
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), blink, RISING);
  delay(1000);
}
void send_command(int cmd){
      Wire.beginTransmission((TWI_BLCTRL_BASEADDR + (0 << 1)) >> 1);
      Wire.write(cmd);
      Wire.endTransmission();
}
void ESC_read(uint8_t *a, uint8_t *b, uint8_t *c, uint8_t *d, uint8_t *e, uint8_t *f) { //, uint8_t *g, uint8_t *h, uint8_t *m){

  Wire.requestFrom((TWI_BLCTRL_BASEADDR + (0 << 1)) >> 1, 6); //read 6 out of 9 bytes, all are uint8_t
  *a = Wire.read(); // Current -> current in 0.1 A steps, read back from BL
  *b = Wire.read(); // MaxPWM -> read back from BL -> is less than 255 if BL is in current limit, not running (250) or starting (40)
  *c = Wire.read(); // Temperature -> old Bl-Ctrl (i.e. earlier than 2.0) will return 255 here, the new version the temp in deg C
  *d = Wire.read(); // RPM -> Raw value for RPM
  *e = Wire.read(); // reserved1 -> Voltage (BL3) or mAh for BL2
  *f = Wire.read(); // Voltage -> in 0.1 V (BL3 is limited to 255, BL2 is only low-byte) ?? What does that mean?
  // Remaining 3 bytes not read
  //*g = Wire.read(); // SlaveI2cError; -> BL2 & BL3
  //*h = Wire.read(); // VersionMajor; -> BL2 & BL3
  //*m = Wire.read(); // VersionMinor; -> BL2 & BL3

  // Print to Serial Monitor: Current MaxPWM Temperature RPM reserved1 Voltage
  Serial.print(cmd);
  Serial.print("\t");
  Serial.print(*a);
  Serial.print("\t");
  Serial.print(*b);
  Serial.print("\t");
  Serial.print(*c);
  Serial.print("\t");
  Serial.print(*d);
  Serial.print("\t");
  Serial.print(*e);
  Serial.print("\t");
  Serial.print(*f);
  Serial.print("\t");

}

void loop() {
  t = 0;
  int i = 0;
  if(cmd>50){
    for (i=0;i<400;i++){
      send_command(30);
      delay(10);
    }
  }
  while(t<t_run){
    send_command(cmd);
    force = analogRead(analogPin);
    byte curr, maxpwm, tmpC, rpm, volt1, volt2;
    ESC_read(&curr, &maxpwm, &tmpC, &rpm, &volt1, &volt2);
    Serial.println(force);
    delay(10);
    t+=20;
  }
  send_command(0);
  delay(t_rest);

  cmd += cmd_step;
  if(cmd>max_cmd){
    while(true){
      send_command(0);
    }
  }
}

void blink() {
  state = !state;
  dt = micros() - timeold;
  timeold = micros();
}
