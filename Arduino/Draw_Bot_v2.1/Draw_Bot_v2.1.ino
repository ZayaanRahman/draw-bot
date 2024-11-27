#include <AccelStepper.h>
#include <math.h>
#include <Wire.h>

#define PI 3.14159265358979323846
#define STEP_PER_MM 12.185
#define MM_PER_RAD 64.5
#define SCALE_FACTOR 10   // Scale factor for converting coordinate scale (cm) to mm

AccelStepper step1(4, 4, 6, 5, 7);      //LEFT   positive - forward 
AccelStepper step2(4, 8, 10, 9, 11);    //RIGHT  positive - backward

int curX = 0, curY = 0, x = 0, y = 0, deltaX, deltaY;

double curDir = (PI / 2);

bool atDestination = true;

int maxSpeed = 600;
int acceleration = 1000;

void setup()
{  
  step1.setMaxSpeed(maxSpeed);          // steps per second
  step1.setAcceleration(acceleration);  // steps per second per second

  step2.setMaxSpeed(maxSpeed);
  step2.setAcceleration(acceleration);

  Serial.begin(9600);

  Wire.begin(0x8);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);

  Serial.println("Setup complete");
}

void receiveEvent(int n) 
{
  // check if n (numBytes) > 1 to ensure enough data is being sent over
  if (n > 1) {
    atDestination = false;

    int bytes[n];

    // fill temp array with sent values
    if (Wire.available()) {
      for (int i = 0; i < n; ++i) {
        bytes[i] = Wire.read();
      }
    }

    // First byte is register address so skip over it
    x = bytes[1] - 128;
    y = bytes[2] - 128;
  }

  // empty input buffer
  while (Wire.available() > 0) {
    Wire.read(); 
  }
}

void requestEvent() 
{
  Wire.write(atDestination ? 1 : 0);
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

    step1.move(-rotSteps);
    step2.move(-rotSteps);

    while(abs(step1.distanceToGo()) > 0 || abs(step2.distanceToGo()) > 0) {
    step1.run();
    step2.run();
    }

    step1.move(magSteps);
    step2.move(-magSteps);

    while(abs(step1.distanceToGo()) > 0 || abs(step2.distanceToGo()) > 0) {
    step1.run();
    step2.run();
    }

    // set robot state to at destination
    curX = x;
    curY = y;
    curDir = dir;
    atDestination = true;

    Serial.print(curX);
    Serial.print(",");
    Serial.print(curY);
    Serial.print(",");
    Serial.println(curDir);
    }
}
