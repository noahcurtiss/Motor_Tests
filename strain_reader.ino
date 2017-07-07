#include "Wire.h"
const byte ledPin = 13;
const byte interruptPin = 2;
volatile byte state = LOW;
volatile int timeold;
volatile int dt= 0;
int analogPin = 0; 
int val = 0;

void setup() {
  Wire.begin();
  delay(1000);
  
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), blink, RISING);
}

void loop() {
  val = analogRead(analogPin);
  Serial.println(val);
   delay(10);
}

void blink() {
  state = !state;
  dt = micros() - timeold;
  timeold = micros();
}
