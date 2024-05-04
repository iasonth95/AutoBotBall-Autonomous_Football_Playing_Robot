#include <Wire.h>
#include <Adafruit_INA219.h>

class CurrentSensor {
  public:
    CurrentSensor(int address);

    float readVoltage(void);
    float readCurrent(void);
    float readPower(void);
    
  private:
    Adafruit_INA219 *ina219;
    int address;
};
