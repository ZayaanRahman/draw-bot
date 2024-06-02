#include <AccelStepper.h>

//const int stepPerRev = 2048;

AccelStepper step1(4, 4, 6, 5, 7);
AccelStepper step2(4, 8, 10, 9, 11);

int x;
int y;

int maxSpeed = 700;
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

  x = analogRead(A0) - 520;
  y = -analogRead(A1) + 509;

  // Serial.print(x);
  // Serial.print(" ");
  // Serial.println(y);

  x = map(x, -510, 510, -maxSpeed, maxSpeed);
  y = map(y, -510, 510, -maxSpeed, maxSpeed);

  step1.setSpeed(y + x);
  step2.setSpeed(-y + x);

  step1.runSpeed();
  step2.runSpeed();
  
}
