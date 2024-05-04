
#ifndef TYPES_H
#define TYPES_H

#include <ArduinoSTL.h>

enum EAction {
  Forward,
  Left,
  Right,
  ReadSensor,
  Grab,
  Slide,
  
  Backward,
  Stop,
  ReadSensor2Current,
  ReadSensor1Power,
  ReadSensor2Power,
  ReadSensor1Voltage,
  ReadSensor2Voltage,
  GrabberClose,
  SliderHigh,
  MotorGetPosition,
  NoChange,
  Err
};

struct Message {
  EAction action;
  uint8_t value;
};

enum ESensorFunction {
  Voltage,
  Current,
  Power
};

enum ESensor {
  Sensor1,
  Sensor2
};

enum EMotor {
  MotorLeft,
  MotorRight
};

enum EServo {
  Grabber,
  Slider
};

#endif
