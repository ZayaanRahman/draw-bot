#include <AccelStepper.h>
#include <math.h>

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
}

void loop()
{
  Serial.println("Enter x and y separated by a space");
  while (Serial.available() == 0) {
  }
  x = Serial.parseInt();
  y = Serial.parseInt();

  Serial.print(x);
  Serial.print(",");
  Serial.println(y);

  // Clear any remaining characters in the input buffer
  while (Serial.available() > 0) {
    char dummy = Serial.read();
  }

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

  // Serial.print("step1 pos: ");
  // Serial.print(step1.currentPosition());
  // Serial.print("  step2 pos: ");
  // Serial.println(step2.currentPosition());
  // delay(1500);

  step1.move(magSteps);
  step2.move(-magSteps);

  while(abs(step1.distanceToGo()) > 0 || abs(step2.distanceToGo()) > 0) {
  step1.run();
  step2.run();
  }

  // Serial.print(x);
  // Serial.print(",");
  // Serial.println(y);

  curX = x;
  curY = y;
  curDir = dir;

  Serial.print(curX);
  Serial.print(",");
  Serial.print(curY);
  Serial.print(",");
  Serial.println(curDir);
  // Serial.print("step1 pos: ");
  // Serial.print(step1.currentPosition());
  // Serial.print("  step2 pos: ");
  // Serial.println(step2.currentPosition());
}
