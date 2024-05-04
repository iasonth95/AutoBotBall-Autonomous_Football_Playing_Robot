#include "decoder.hpp"

Decoder::Decoder(void){
  bluetooth = new SoftwareSerial(0, 1); // RX | TX  
  bluetooth->begin(38400);

  addMessage(0x03, EAction::Right);
  addMessage(0x01, EAction::Slide);
  addMessage(0x02, EAction::Forward);
  addMessage(0x04, EAction::Left);
  addMessage(0x05, EAction::ReadSensor);
  addMessage(0x06, EAction::Grab);

}

struct Message Decoder::getLatestMessage(void){
  String msg = "";
  while(1){
    if (Serial.available()) {
      delay(10);
      while (Serial.available() > 0) {
        msg += (char)Serial.read();
      }
      Serial.flush();
      latestMessage = decodeBluetoothMessage(msg[0]);
      return latestMessage;
    }
  }
}

struct Message Decoder::decodeBluetoothMessage(const char state){
  Message mes;
  mes.action = EAction::Err;
  mes.value = 0;
  
  std::map<char, EAction>::iterator it;
   for(it = messageMap.begin(); it != messageMap.end(); ++it){
      if(!(it->first ^ (state&0x07))){
        mes.action = it->second;
        mes.value = (state >> 3) & 0x1F;
      }
   }
   return mes;

   
}

void Decoder::addMessage(const char character, const EAction message){
  messageMap.insert({ character, message });
}
