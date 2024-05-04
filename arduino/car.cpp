#include "car.hpp"

#define PWM_L 6
#define PWM_R 5
#define EN_L_BWD 8
#define EN_L_FWD 4
#define EN_R_BWD 12
#define EN_R_FWD 7

#define HAL_L_A 2
#define HAL_L_B 10
#define HAL_R_A 3
#define HAL_R_B 11

#define SENSOR_1_ADDRESS 0x40
#define SENSOR_2_ADDRESS 0x41

#define SERVO_GRABBER_PIN 9
#define SERVO_SLIDER_PIN 13

Car::Car(){
  motorRight = new Motor(EMotor::MotorLeft, PWM_L, EN_L_FWD, EN_L_BWD, HAL_R_A, HAL_R_B);
  motorLeft = new Motor(EMotor::MotorRight, PWM_R, EN_R_FWD, EN_R_BWD, HAL_L_A, HAL_L_B);

  sens1 = new CurrentSensor(SENSOR_1_ADDRESS);
  sens2 = new CurrentSensor(SENSOR_2_ADDRESS);
  
  grabber.attach(SERVO_GRABBER_PIN);
  slider.attach(SERVO_SLIDER_PIN);
  
  setServoPosition(EServo::Slider,0);
  setServoPosition(EServo::Grabber, 0);
}
 
Car::~Car(){
  delete motorLeft;
  delete motorRight;
  delete sens1;
  delete sens2;
}

void Car::move1(long int setPosL, long int setPosR, EAction mess){
  float eR = 0.0, eL = 0.0, eDiff = 0.0, uDiff = 0.0, eintegralR = 0.0, eintegralL = 0.0, eintegralDiff = 0.0, pwrL = 0.0, pwrR = 0.0;
  long int posL = 0, posR = 0;
  bool reachedL = false, reachedR = false;
  
  unsigned long prevT = micros();
  
  long int setPosLPositive = abs(setPosL);
  long int setPosRPositive = abs(setPosR);
  
  int maxR = Kp*setPosRPositive;
  int maxL = Kp*setPosLPositive;

  getRestore(EMotor::MotorLeft);
  getRestore(EMotor::MotorRight);
  
  do{
    unsigned long currentT = micros();
    float deltaT = ((float) (currentT-prevT))/1.0e6;
    prevT = currentT;

    // PI to calculate right motor speed
    posR = getMotorPWM(EMotor::MotorRight, mess);
    eR = setPosRPositive - abs(posR);
    eintegralR= eintegralR + eR*deltaT;
    float uR = Kp*eR + Ki*eintegralR;
    pwrR=map(abs(uR),0,maxR,200,220);

    // PI to calculate left motor speed
    posL = getMotorPWM(EMotor::MotorLeft, mess);
    eL = setPosLPositive - abs(posL);
    eintegralL= eintegralL + eL*deltaT;
    float uL = Kp*eL + Ki*eintegralL; 
    pwrL=map(abs(uL),0,maxL,200,220);  

    if(setPosLPositive == setPosRPositive){
      // PI to go straight
      eDiff = abs(posL) - abs(posR);
      eintegralDiff= eintegralDiff + eDiff*deltaT;
      uDiff = Kp*eDiff + Ki*eintegralDiff; 
  
      if(uDiff > 0){ // Left wheel is going faster then right wheel
        pwrR += abs(uDiff*2);
        
      }else{
        pwrL += abs(uDiff*2);
      }
    }
    if(pwrR > 255){
      pwrR = 255; 
    }
   
    if(pwrL > 255){
      pwrL = 255; 
    }

    // Check if right motor has reached desitnation
    if(abs(eR) < 25){
      reachedR = true;
      motorRight->setMotor(0);
          }

    // Check if left motor has reached desitnation
    if(abs(eL) < 25){
      reachedL = true;
      motorLeft->setMotor(0);
          }
      
    if(!reachedR){
      if(setPosR<0){
        motorRight->setMotor(-1*pwrR);
      }else{
        motorRight->setMotor(pwrR);
      }
    }

    if(!reachedL){
      if(setPosL<0){
        motorLeft->setMotor(-1*pwrL);
      }else{
        motorLeft->setMotor(pwrL);
      }
    }

    Serial.println(String(readSensor(ESensor::Sensor2, ESensorFunction::Voltage)) + " " + String(readSensor(ESensor::Sensor2, ESensorFunction::Current)) + " " + String(readSensor(ESensor::Sensor2, ESensorFunction::Power)));
    
  }while(!reachedL || !reachedR);
    
}

float Car::readSensor(ESensor sensor, ESensorFunction function){
  CurrentSensor* temp = (sensor == ESensor::Sensor1) ? sens1 : sens2;

  switch(function){
    case ESensorFunction::Voltage:
      return temp->readVoltage();
      break;
    case ESensorFunction::Current:
      return temp->readCurrent();
      break;
    case ESensorFunction::Power:
      return temp->readPower();
      break;
    default:
      return 0.69;
      break;
  }
}

void Car::setServoPosition(const EServo servo, const int pos){
  if(servo == EServo::Grabber){
    Serial.println("Grab: " + String(pos) + " " + String(readSensor(ESensor::Sensor2, ESensorFunction::Voltage)) + " " + String(readSensor(ESensor::Sensor2, ESensorFunction::Current)) + " " + String(readSensor(ESensor::Sensor2, ESensorFunction::Power)));
    grabber.write(pos);
    Serial.println("Grab: " + String(pos) + " " + String(readSensor(ESensor::Sensor2, ESensorFunction::Voltage)) + " " + String(readSensor(ESensor::Sensor2, ESensorFunction::Current)) + " " + String(readSensor(ESensor::Sensor2, ESensorFunction::Power)));
  }else{
    if((!sliderPosition && pos < SLIDER_STOP) || (sliderPosition && pos > SLIDER_STOP)){
      //do nothing
    }else if(pos!=SLIDER_STOP){
      Serial.println("slide: " + String(pos) + " " + String(readSensor(ESensor::Sensor2, ESensorFunction::Voltage)) + " " + String(readSensor(ESensor::Sensor2, ESensorFunction::Current)) + " " + String(readSensor(ESensor::Sensor2, ESensorFunction::Power)));
      slider.writeMicroseconds(pos);
    Serial.println("slide: " + String(pos) + " " + String(readSensor(ESensor::Sensor2, ESensorFunction::Voltage)) + " " + String(readSensor(ESensor::Sensor2, ESensorFunction::Current)) + " " + String(readSensor(ESensor::Sensor2, ESensorFunction::Power)));
      sliderPosition = !sliderPosition;
    }else if (pos==SLIDER_STOP){
      Serial.println("slide: " + String(pos) + " " + String(readSensor(ESensor::Sensor2, ESensorFunction::Voltage)) + " " + String(readSensor(ESensor::Sensor2, ESensorFunction::Current)) + " " + String(readSensor(ESensor::Sensor2, ESensorFunction::Power)));
      slider.writeMicroseconds(pos);
      Serial.println("slide: " + String(pos) + " " + String(readSensor(ESensor::Sensor2, ESensorFunction::Voltage)) + " " + String(readSensor(ESensor::Sensor2, ESensorFunction::Current)) + " " + String(readSensor(ESensor::Sensor2, ESensorFunction::Power)));
    } else{
      Serial.println("d");
    }
  }
}

long Car::getMotorPosition(EMotor motor){
  Motor* temp = (motor == EMotor::MotorLeft) ? motorLeft : motorRight;
  return temp->getPosition();
}

long Car::getMotorPWM(EMotor motor, EAction mess){
  Motor* temp = (motor == EMotor::MotorLeft) ? motorLeft : motorRight;
  return temp->getPWM(mess);
}
long Car::getMotorDiff(EMotor motor){
  Motor* temp = (motor == EMotor::MotorLeft) ? motorLeft : motorRight;
  return temp->getDiff();
}

long Car::getRestore(EMotor motor){
  Motor* temp = (motor == EMotor::MotorLeft) ? motorLeft : motorRight;
  return temp->restore();
}
