#include "decoder.hpp"
#include "car.hpp"

#define CM_TO_PULSE(x) (912*x)/25 // 25: circumference
#define ANGLE_TO_PULSE(x) (2465*x)/180

Decoder *decoder;
Car *car;
//Motor *motor;
void setup() {
  Serial.begin(38400);  
  //Serial.println("Ready to connect\nDefault password is 1234 or 0000"); 
  //Serial.flush();
  decoder = new Decoder();
  car = new Car();
  //motor = new Motor();

  // Send it twice, because weird reasons....
  Serial.println(0x10 >> 3, BIN); // (10011)111 -> ready message should have 3x 1's at the beginning
  Serial.println("O"); // (10011)111 -> ready message should have 3x 1's at the beginning

  
}

void loop() 
{ 
  struct Message message = decoder->getLatestMessage();
  unsigned int dis =  0;
  unsigned long step1 = 0;
  unsigned long step2 = 0;
  switch(message.action){
    case EAction::Forward:
      //Serial.println("FORWARD " + String(message.value));
      step1 = (message.value*3);
      step2 = (921*step1);
      dis = (unsigned int)(step2/25);
      Serial.println("Dis: " + String(dis) + "mes val: " + String(message.value) + "step1 " + step1 + " step 2 " + step2 );
      car->move1(-1*(int)dis, -1*(int)dis, EAction::Forward );
      break;
    case EAction::Left:
      //Serial.println("LEFT " + String(message.value));
      step1 = (message.value*3);
      step2 = (2465*step1);
      dis = (unsigned int)(step2/180);
      //Serial.println(dis);
      Serial.println("Dis: " + String(dis) + "mes val: " + String(message.value) + "step1 " + step1 + " step 2 " + step2 +"\n");
      car->move1(-1*(int)dis, (int)dis, EAction::Left);
      break;
    case EAction::Right:
      //Serial.println("RIGHT " + String(message.value));
      step1 = (message.value*3);
      step2 = (2465*step1);
      dis = (unsigned int)(step2/180);
      //Serial.println(dis);
      Serial.println("Dis: " + String(dis) + "mes val: " + String(message.value) + "step1 " + step1 + " step 2 " + step2 );
      car->move1((int)dis, -1*(int)dis, EAction::Right);
      break;
    case EAction::ReadSensor:
      if(message.value == 0){
        Serial.println(String(car->readSensor(ESensor::Sensor1, ESensorFunction::Current)));
        //Serial.println("sensor value 0");
      }else if(message.value == 1){
        //Serial.println("sensor value 1");
        Serial.println(String(car->readSensor(ESensor::Sensor2, ESensorFunction::Current)));
      }else if(message.value == 2){
        //Serial.println("sensor value 2");
        Serial.println(String(car->readSensor(ESensor::Sensor1, ESensorFunction::Voltage)));
      }else if(message.value == 3){
        //Serial.println("sensor value 3");
        Serial.println(String(car->readSensor(ESensor::Sensor2, ESensorFunction::Voltage)));
      }else if(message.value == 4){
        //Serial.println("sensor value 4");
        Serial.println(String(car->readSensor(ESensor::Sensor1, ESensorFunction::Power)));
      }else if(message.value == 5){
        //Serial.println("sensor value 5");
        Serial.println(String(car->readSensor(ESensor::Sensor2, ESensorFunction::Power)));
      }
      //Serial.println("read sensor 1 current: "  + String(message.value));
      break;
    case EAction::Grab:
      if(message.value == 0){
      //Serial.println("Grabber Closed");
        car->setServoPosition(EServo::Grabber, 0);
      }else{
      //Serial.println("Grabber Open");
        car->setServoPosition(EServo::Grabber, 115);
      }
      break;
    case EAction::Slide:
      if(message.value == 0){
        //Serial.println("Slider Low");
        car->setServoPosition(EServo::Slider, 1000);
        delay(2050);
        car->setServoPosition(EServo::Slider, SLIDER_STOP);
      }else{
        //Serial.println("Slider High");
        car->setServoPosition(EServo::Slider, 2000);
        delay(2125);
        car->setServoPosition(EServo::Slider, SLIDER_STOP);
      }
      break;
      
    /*case EMessage::ReadSensor2Current:
      Serial.println("read sensor 2 current: " + String(car->readSensor(ESensor::Sensor2, ESensorFunction::Current)));
      break;
    case EMessage::ReadSensor1Power:
      Serial.println("read sensor 1 power: " + String(car->readSensor(ESensor::Sensor1, ESensorFunction::Power)));
      break;
    case EMessage::ReadSensor2Power:
      Serial.println("read sensor 2 power: " + String(car->readSensor(ESensor::Sensor2, ESensorFunction::Power)));
      break;
    case EMessage::ReadSensor1Voltage:
      Serial.println("read sensor 1 voltage: " + String(car->readSensor(ESensor::Sensor1, ESensorFunction::Voltage)));
      break;
    case EMessage::ReadSensor2Voltage:
      Serial.println("read sensor 2 voltage: " + String(car->readSensor(ESensor::Sensor2, ESensorFunction::Voltage)));
      break;
    case EMessage::GrabberOpen:
      Serial.println("Grabber Open");
      car->setServoPosition(EServo::Grabber, 0);
      break;
    case EMessage::GrabberClose:
      Serial.println("Grabber Close");
      car->setServoPosition(EServo::Grabber, 90);
      break;
    case EMessage::SliderLow: //p
      Serial.println("Slider Low");
      car->setServoPosition(EServo::Slider, 1000);//1000
      delay(2050);
      car->setServoPosition(EServo::Slider, SLIDER_STOP);//stop
      break;
    case EMessage::SliderHigh: //q
      Serial.println("Slider High");
      car->setServoPosition(EServo::Slider, 2000);//2000
      delay(2125);
      car->setServoPosition(EServo::Slider, SLIDER_STOP);//stop
      break;
    case EMessage::MotorGetPosition:
      //Serial.println("Motor left: " + String(car->getMotorPosition(EMotor::MotorLeft)) + ", motor right: " + String(car->getMotorPosition(EMotor::MotorRight))+ ", diff" + String(car->getMotorDiff(EMotor::MotorRight))+ ", diff" + String(car->getMotorDiff(EMotor::MotorLeft)) + "rwheel" + String(rightWheel)+ "lwheel" +String(leftWheel));
      //Serial.println("left: "+ String(car->getMotorPWM(EMotor::MotorLeft)) + ", right: " + String(car->getMotorPWM(EMotor::MotorRight)) + ", diff" + String(car->getMotorDiff(EMotor::MotorRight))+ ", diff" + String(car->getMotorDiff(EMotor::MotorLeft)));
      break;*/
    default:
      break;
  }
  Serial.println("O"); // (10011)111 -> ready message should have 3x 1's at the beginning
  delay(500);
}
