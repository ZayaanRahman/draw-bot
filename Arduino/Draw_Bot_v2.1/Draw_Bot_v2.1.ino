#include <AccelStepper.h>
#include <math.h>
#include <Wire.h>

#define addr 0x8
#define PI 3.14159265358979323846
#define STEP_PER_MM 12.185
#define MM_PER_RAD 64.5
#define SCALE_FACTOR 10   // Scale factor for converting coordinate scale (cm) to mm

AccelStepper step1(4, 4, 6, 5, 7);      //LEFT   positive - forward 
AccelStepper step2(4, 8, 10, 9, 11);    //RIGHT  positive - backward

int curX = 0, curY = 0, x = 0, y = 0, deltaX, deltaY;

double curDir = (PI / 2);

int maxSpeed = 600;
int acceleration = 1000;

void setup()
{  
  step1.setMaxSpeed(maxSpeed);          // steps per second
  step1.setAcceleration(acceleration);  // steps per second per second

  step2.setMaxSpeed(maxSpeed);
  step2.setAcceleration(acceleration);

  Serial.begin(9600);
  Serial.println("ON");

  Wire.begin(addr);
  Wire.onReceive(receiveEvent);
}

void receiveEvent() {
  Serial.print(x);
  Serial.print(", ");
  Serial.println(y);
  
  while (Wire.available()) {
    char xVal = Wire.read();            // Bytes read as chars so they are cast as signed ints
    x = (int) xVal;

    char yVal = Wire.read();
    y = (int) yVal;
  }

  Serial.print(x);
  Serial.print(", ");
  Serial.println(y);

  Wire.beginTransmission(addr);
  Wire.write("WAIT");
  Wire.endTransmission();
}

void loop()
{
  if (x != curX || y != curY) {
    Serial.print(x);
    Serial.print(",");
    Serial.println(y);

    deltaX = x - curX, deltaY = y - curY;

    double mag = sqrt(square(deltaX) + square(deltaY));

    double dir = atan2( (double) deltaY, (double) deltaX);

    long rotSteps = round((dir - curDir) * MM_PER_RAD * STEP_PER_MM);

    long magSteps = round(mag * SCALE_FACTOR * STEP_PER_MM);

    Wire.beginTransmission(addr);
    Wire.write("WAIT");
    Wire.endTransmission();

    step1.move(-rotSteps);
    step2.move(-rotSteps);

    while(abs(step1.distanceToGo()) > 0 || abs(step2.distanceToGo()) > 0) {
    step1.run();
    step2.run();
    }

    Wire.beginTransmission(addr);
    Wire.write("WAIT");
    Wire.endTransmission();

    step1.move(magSteps);
    step2.move(-magSteps);

    while(abs(step1.distanceToGo()) > 0 || abs(step2.distanceToGo()) > 0) {
    step1.run();
    step2.run();
    }

    curX = x;
    curY = y;
    curDir = dir;

    Wire.beginTransmission(addr);
    Wire.write("DONE");
    Wire.endTransmission();

    Serial.print(curX);
    Serial.print(",");
    Serial.print(curY);
    Serial.print(",");
    Serial.println(curDir);
    }
}
