#include <Wire.h>

#define addr 0x8

// Global boolean variable
bool is_ready = true;

void setup()
{
    Serial.begin(9600);
    Serial.println("ON");

    Wire.begin(addr);
    Wire.onReceive(receiveEvent);
    Wire.onRequest(requestEvent);
}

void receiveEvent(int n)
{
    if (!is_ready)
    {
        Serial.println("Bytes sent when not ready, incorrect behavior");
        return;
    }
    // if is_ready is true, process the numbers sent

    is_ready = false;

    int x = 999;
    int y = 999;

    if (Wire.available())
    {
        int xByte = Wire.read();
        x = (xByte)-128; // not sure whether to use int or char, try this
    }
    else
    {
        Serial.println("Failed to get x byte");
    }

    if (Wire.available())
    {
        int yByte = Wire.read();
        y = (yByte)-128; // not sure whether to use int or char
    }
    else
    {
        Serial.println("Failed to get y byte");
    }

    if (x != 999 && y != 999)
    {
        Serial.print("Success reading both bytes: ");
    }
    else
    {
        Serial.print("Failure reading bytes: ");
    }

    Serial.print(x);
    Serial.print(", ");
    Serial.println(y);

    is_ready = true; // allow pi to recieve a 1 on next request
}

void requestEvent()
{
    int returnByte = is_ready ? 1 : 0;
    Wire.write(returnByte);
}

void loop()
{
    delay(200);
}