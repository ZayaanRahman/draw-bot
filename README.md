# draw-bot
Working on a robot that follows a hand drawn path from a web interface 🤖

## General Idea:
The robot will be controlled by an Arduino microcontroller and a RaspberryPi. The Pi adds points to its path from the CLI or the path drawn and sent from the web GUI. As the points are proccessed and added to a queue, they are sent to the Arduino, which guides the robot through points.

## What's Done:
- Hardware
- Pi code
- Arduino code
- CLI
- Web GUI

## What's Left:
- I2C communication
- Assemble and test
