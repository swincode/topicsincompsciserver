# Machine_2 - Picker
This machine was created to approximate a machine moving an item from the scanner to the next part of the manifacturing process. When a signal is received, each servo is moved to a position of 180 degrees, then returns to the baseline position of 0 degrees.  
The red LED is added to signify when the machine has received data and is working on an item.

## Components
- Arduino Uno
- Red LED
- 220 Ohm Resistor
- 2x 9g Tower Pro Micro Servo Motors  
- 5v Voltage Regulator
- Ceramic Capacitor 100nF
- Electrolytic Capacitor 1nF

## Requirements
This machine utilises the Adafruit Servo library that can be installed via the Arduino IDE.
```Tools -> Manage Libraries -> Servo v1.1.6```
[Reference Manual](https://www.arduino.cc/reference/en/libraries/servo/)


## Wiring Diagram

![](https://github.com/swincode/topicsincompsciserver/blob/main/machine_2/machine_2_diagram.png)
