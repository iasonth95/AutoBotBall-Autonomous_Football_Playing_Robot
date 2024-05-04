#include <SoftwareSerial.h> 
#include <ArduinoSTL.h>
#include <map>

#include "types.h"

class Decoder {
  public:
    Decoder(void);
    struct Message getLatestMessage(void);

  private:
    struct Message latestMessage;
    SoftwareSerial *bluetooth;
    struct Message decodeBluetoothMessage(const char state);

    void addMessage(const  char character, const EAction message);

    std::map<char, EAction> messageMap;
};
