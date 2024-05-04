#include "currentSensor.hpp"

CurrentSensor::CurrentSensor(int _address){
  address= _address;
  ina219 = new Adafruit_INA219(address);
  if (!ina219->begin()) {
    Serial.println("Failed to find INA219 chip");
  }
}

float CurrentSensor::readVoltage(void){
  return ina219->getBusVoltage_V();
}

float CurrentSensor::readCurrent(void){
  return ina219->getCurrent_mA();
}

float CurrentSensor::readPower(void){
  return ina219->getPower_mW();
}
