# draw-bot
Working on a robot that follows a hand drawn path from a web interface 🤖

## Outline:
The robot will be controlled by an Arduino microcontroller and a RaspberryPi. The Pi will listen for commands from the server and instruct the arduino to move the robot towards the points specified in its point queue. The server will be responsible for receiving the path from the web interface, processing it into a series of points, and sending those points to the Pi. The robot can also be controlled via CLI on the server.

## What's Done:
- Pi code
- Server code
- Server CLI
