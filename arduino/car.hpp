#include "types.h"
#include "motor.hpp"
#include "currentSensor.hpp"
#include <Servo.h>

#define SLIDER_STOP 1500 //1540

class Car {
  public:
    Car();
    ~Car();
    
    void move(int leftWheelSpeed, int rightWheelSpeed, EAction mess);
    void move1(long int setPosL, long int setPosR, EAction mess);
    float readSensor(ESensor sensor, ESensorFunction function);  
    void setServoPosition(const EServo servo, const int pos);
    long getMotorPosition(EMotor motor);
    long getMotorPWM(EMotor motor, EAction mess);
    long getMotorDiff(EMotor motor);

    long getRestore(EMotor motor);

    
  private:
    Motor *motorLeft;
    Motor *motorRight;
    
    CurrentSensor *sens1;
    CurrentSensor *sens2; 
    
    Servo grabber;
    Servo slider;

    bool sliderPosition = false; // True: high, False: low

    const double Kp = 0.1;
    const double Ki = 0.005;
};

  
