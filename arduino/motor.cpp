#include "motor.hpp"

Motor::Motor(const EMotor _motorType, unsigned char _cucPWM, const unsigned char _cucFWD, const unsigned char _cucBWD, const unsigned char _encoderPinA, const unsigned char _encoderPinB){
  cucPWM = _cucPWM;
  cucFWD = _cucFWD;
  cucBWD = _cucBWD;

  pinMode(_encoderPinA, INPUT);
  pinMode(_encoderPinB, INPUT);

  motorType = _motorType;
  
  if(motorType == EMotor::MotorLeft){
    attachInterrupt(digitalPinToInterrupt(_encoderPinA), interruptFuncMotorLeft, CHANGE);
    encoderPinALeft = _encoderPinA;
    encoderPinBLeft = _encoderPinB;
  } else{
    attachInterrupt(digitalPinToInterrupt(_encoderPinA), interruptFuncMotorRight, CHANGE);
    encoderPinARight = _encoderPinA;
    encoderPinBRight = _encoderPinB;
  }

  pinMode(13,OUTPUT);
 
  analogWrite(_cucPWM, 0); 
  digitalWrite(_cucFWD, LOW);
  digitalWrite(_cucBWD, LOW);

  pinMode(_cucPWM, OUTPUT);
  pinMode(_cucFWD, OUTPUT);
  pinMode(_cucBWD, OUTPUT);
}

int Motor::setMotor(int ciSpeed)
{
  if (ciSpeed < 0)
  {
    digitalWrite(cucFWD, LOW);
    digitalWrite(cucBWD, LOW); 
    digitalWrite(cucFWD, LOW);
    digitalWrite(cucBWD, HIGH); 
  }
  else
  {
    digitalWrite(cucFWD, LOW);
    digitalWrite(cucBWD, LOW); 
    digitalWrite(cucFWD, HIGH);
    digitalWrite(cucBWD, LOW); 
  }

  analogWrite(cucPWM, abs(ciSpeed));  
  return ciSpeed;
}

long Motor::getPosition(){
  if(motorType == EMotor::MotorLeft){
    return (positionLeft * -1);
  }
  return positionRight;
}

long Motor::getPWM(EAction mess){
  if(motorType == EMotor::MotorRight){
    if(mess == EAction::Backward || mess==EAction::Left){
      return count_right;
    }
    return -count_right;
  }
   
  if(mess == EAction::Backward || mess==EAction::Right){
      return count_left;
    }
  return -count_left;
}

int Motor::getDiff(){
    int diff = count_left-count_right;
  return diff;
}

long Motor::restore(){
  if(motorType == EMotor::MotorLeft){
    count_left = 0;
    positionLeft = 0;
    return count_left;
  }
  count_right = 0;
  positionRight = 0;
  return count_right;
}

float Motor::getLinearToAngularVelocity(float forward, float rotation){
    auto forward_vel = forward / wheelRadius;
    auto rotation_vel = (0.5f*interwheelDistance*rotation) / wheelRadius;
    if(motorType == EMotor::MotorLeft){
    return forward_vel - rotation_vel;
    }
    return forward_vel + rotation_vel;
    }
