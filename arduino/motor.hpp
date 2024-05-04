#include "Arduino.h"
#include "types.h"
class Motor {
  public:
    Motor(const EMotor motorType, unsigned char cucPWM, const unsigned char cucFWD, const unsigned char cucBWD, const unsigned char encoderPinA, const unsigned char encoderPinB);
    int setMotor(int ciSpeed);

    long getPosition();
    long getPWM(EAction mess);
    int getDiff();
    long restore();
    float getLinearToAngularVelocity(float forward, float rotation);
    //long getAngularVelocity();
    //float v;
    //unsigned long prevT = 0; // microseconds
    //unsigned long prevpos = 0;
    //long pos;
    
  private:
    unsigned char cucPWM;
    unsigned char cucFWD;
    unsigned char cucBWD;
    EMotor motorType;
};

const double MAX_ANGULAR_VELOCITY = 2*M_PI;     //[rad/s] = 0.5 rotation/s
const double MAX_ROTATION_VEL = 0.0698f * 8;    //[rads/s] = ~4*8 = ~32 degrees/s
const double MAX_TRANSLATE_VEL = 0.125f * 1.5;  //[m/s]

//translate_vel_setpoint = min(max(command.value, -MAX_TRANSLATE_VEL), MAX_TRANSLATE_VEL);
//rotate_vel_setpoint = min(max(command.value, -MAX_ROTATION_VEL), MAX_ROTATION_VEL);





static unsigned char encoderPinALeft;
static unsigned char encoderPinBLeft;
static long positionLeft = 0;

static unsigned char encoderPinARight;
static unsigned char encoderPinBRight;
static long positionRight = 0;

static int diameter = 74;
static int circumference = 25; //diameter * M_PI;
static long pulses = (12*300)/circumference;

// Physical constants
const float wheelRadius = 0.04;         //[m]
const float interwheelDistance = 0.42;  //[m]
const float encoderCalibrationConstant = 1000.0/833.0;  // Expected 1000mm, got 833mm
const int encoderCountsPerRotation = encoderCalibrationConstant * 32 * 12 * 2;
constexpr float radiansPerEncoderTick = 2*M_PI / (2*encoderCountsPerRotation); //2pi/T why 2 ?


//unsigned long prevMeasurementTime; // microseconds
//int encoderCountsPerRotation;
//static unsigned long timeMotorRight;


static unsigned long timeMotorRight;
static int count_right;
static int count_left;
//static int diff;

static void interruptFuncMotorLeft() { 
  //if (count_right > count_left){
    //static int error = count_right - count_left;
  //}
  
    count_left++;
  //diff = count_left-count_right;
  //Interrupt function to read the x2 pulses of the encoder.
  if ( digitalRead(encoderPinBLeft) == 0 ) {
    if ( digitalRead(encoderPinALeft) == 0 ) {
      // A fell, B is low
      positionLeft--; // Moving forward
    } else {
      // A rose, B is high
      positionLeft++; // Moving reverse
    }
  } else {
    if ( digitalRead(encoderPinALeft) == 0 ) {
      positionLeft++; // Moving reverse
    } else {
      // A rose, B is low
      positionLeft--; // Moving forward
    }
  }

}

static void interruptFuncMotorRight() { 
  //unsigned long currentTime = millis();
  count_right++;
  //diff = count_left-count_right;
  //unsigned long difference = count_left - count_right;
  //if(currentTime<=60000){
    if(count_right % 12 == 0){
      //counttt = 0;
      //countrpm++;

      //Serial.println("left: "+ String(count_left) + ", right " + String(count_right) + ", circumference:" + String(circumference));
   }
  //}
    
 //float rpm = 100/(difference * 1000);

    //timeMotorRight = currentTime;
  
  //Interrupt function to read the x2 pulses of the encoder.
  if ( digitalRead(encoderPinBRight) == 0 ) {
    if ( digitalRead(encoderPinARight) == 0 ) {
      // A fell, B is low
      positionRight--; // Moving forward
    } else {
      // A rose, B is high
      positionRight++; // Moving reverse
    }
  } else {
    if ( digitalRead(encoderPinARight) == 0 ) {
      positionRight++; // Moving reverse
    } else {
      // A rose, B is low
      positionRight--; // Moving forward
    }
  }

}
